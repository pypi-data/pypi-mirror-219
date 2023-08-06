from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple

import fsspec
import fugue.api as fa
import fugue.column as fc
import pandas as pd
from fugue import AnyDataFrame

from fugue_ml.utils.registry import fugue_ml_plugin

_EMBEDDING_CACHE_UID = "embedding_uid"
_EMBEDDING_CACHE_VEC = "embedding_vec"


@fugue_ml_plugin
def parse_embedding_cache(cache: Any, **kwargs: Any) -> "EmbeddingCache":
    if isinstance(cache, EmbeddingCache):
        return cache
    raise ValueError(f"unrecognized embedding cache {cache}")


@parse_embedding_cache.candidate(
    lambda cache, **kwargs: isinstance(cache, str) and cache.startswith("file:")
)
def _parse_local_file_embedding_cache(cache: Any, **kwargs: Any) -> "EmbeddingCache":
    path = cache.split(":", 1)[1]
    return FileEmbeddingCache(path)


class EmbeddingCache(ABC):
    @abstractmethod  # pragma: no cover
    def query_ids(self, ids: AnyDataFrame) -> Optional[AnyDataFrame]:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def upsert_ids(self, ids: AnyDataFrame) -> None:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def clear(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod  # pragma: no cover
    def can_check_count(self) -> bool:
        return False

    def __enter__(self) -> "EmbeddingCache":
        return self

    def __exit__(self, *args: Any) -> None:
        self.clear()

    def query(
        self, df: AnyDataFrame, uid_col: str, vec_col: str
    ) -> Tuple[Optional[AnyDataFrame], Optional[AnyDataFrame]]:
        ids = fa.select_columns(df, [uid_col])
        found = self.query_ids(fa.rename(ids, {uid_col: _EMBEDDING_CACHE_UID}))
        if found is None:
            return None, df
        found = fa.rename(
            found, {_EMBEDDING_CACHE_UID: uid_col, _EMBEDDING_CACHE_VEC: vec_col}
        )
        res = fa.left_outer_join(df, found)
        cached = fa.filter(res, ~fc.col(vec_col).is_null())
        df = fa.select(
            res,
            *[fc.col(x) for x in fa.get_column_names(df)],
            where=fc.col(vec_col).is_null(),
        )
        if self.can_check_count and fa.count(df) == 0:
            return cached, None
        return cached, df

    def find_new(self, df: AnyDataFrame, uid_col: str) -> AnyDataFrame:
        ids = fa.select_columns(df, [uid_col])
        cached = self.query_ids(fa.rename(ids, {uid_col: _EMBEDDING_CACHE_UID}))
        if cached is None:
            return df
        cached_ids = fa.rename(
            fa.select_columns(cached, [_EMBEDDING_CACHE_UID]),
            {_EMBEDDING_CACHE_UID: uid_col},
        )
        return fa.anti_join(df, cached_ids)

    def upsert(self, df: AnyDataFrame, uid_col: str, vec_col: str) -> None:
        ids = fa.select_columns(df, [uid_col, vec_col])
        self.upsert_ids(
            fa.rename(
                ids, {uid_col: _EMBEDDING_CACHE_UID, vec_col: _EMBEDDING_CACHE_VEC}
            )
        )


class PandasEmbeddingCache(EmbeddingCache):
    def __init__(self, init_cache: Optional[pd.DataFrame] = None) -> None:
        super().__init__()
        self.cache: Optional[pd.DataFrame] = init_cache

    @property
    def can_check_count(self) -> bool:
        return True

    def query_ids(self, ids: AnyDataFrame) -> Optional[AnyDataFrame]:
        if self.cache is None or len(self.cache) == 0:
            return None
        q = fa.as_pandas(ids).dropna().drop_duplicates()
        return fa.semi_join(self.cache, q)

    def upsert_ids(self, ids: AnyDataFrame) -> None:
        if self.cache is None:
            self.cache = fa.as_pandas(ids)
            return
        new_df = fa.as_pandas(ids).assign(rank=0)
        tdf = pd.concat([self.cache.assign(rank=1), new_df])
        tdf = fa.take(tdf, n=1, presort="rank", partition=_EMBEDDING_CACHE_UID)
        tdf = fa.drop_columns(tdf, ["rank"])
        self.cache = fa.as_pandas(tdf)

    def clear(self) -> None:
        self.cache = None


class FileEmbeddingCache(EmbeddingCache):
    def __init__(self, path) -> None:
        super().__init__()
        self.path = path

    @property
    def can_check_count(self) -> bool:
        return True

    def query_ids(self, ids: AnyDataFrame) -> Optional[AnyDataFrame]:
        fs, path = fsspec.core.url_to_fs(self.path)
        if not fs.exists(path):
            return None
        tdf = pd.read_parquet(self.path).reset_index(drop=True)
        q = fa.as_pandas(ids).dropna().drop_duplicates()
        return fa.semi_join(tdf, q)

    def upsert_ids(self, ids: AnyDataFrame) -> None:
        new_df = fa.as_pandas(ids)
        fs, path = fsspec.core.url_to_fs(self.path)
        if not fs.exists(path):
            new_df.to_parquet(self.path)
        else:
            tdf = pd.read_parquet(self.path)
            new_df = new_df.assign(rank=0)
            tdf = pd.concat([tdf.assign(rank=1), new_df])
            tdf = fa.take(tdf, n=1, presort="rank", partition=_EMBEDDING_CACHE_UID)
            tdf = fa.drop_columns(tdf, ["rank"])
            fa.as_pandas(tdf).to_parquet(self.path)

    def clear(self) -> None:
        fs, path = fsspec.core.url_to_fs(self.path)
        fs.rm(path)
