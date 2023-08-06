import os
import pickle
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, Union
from uuid import uuid4

import fsspec
import fugue.api as fa
import numpy as np
import pandas as pd
from fugue import AnyDataFrame
from triad import Schema, assert_or_throw
from triad.utils.batch_reslicers import PandasBatchReslicer
from triad.utils.convert import to_size
from triad.utils.threading import SerializableRLock
from fugue_ml.utils.fugue_ext import (
    deterministic_shard,
    replicate,
    deterministic_shard_and_replicate,
)
from fugue_ml.utils.io import unzip_to_temp, zip_temp
from fugue_ml.utils.registry import fugue_ml_plugin
from fugue_ml.utils.schema import is_vec_col

_INDEXERS: Dict[str, Type["KNNIndexer"]] = {}
_INDEXER_ATTR = "_indexer_name"
_INDEXER_BLOB_COLUMN_NAME = "_indexer_blob"
_INDEXER_REPLICATES_COLUMN_NAME = "_indexer_rep"
_INDEXER_SHARD_COLUMN_NAME = "_indexer_shard"
_TEMP_DIST_COL = "_temp_dist"


def register_knn_indexer(name: str) -> Callable:
    def deco(cls: Type) -> Type:
        assert_or_throw(
            issubclass(cls, KNNIndexer),
            TypeError(f"{cls} is not a subtype of KNNIndexer"),
        )
        assert_or_throw(
            name not in _INDEXERS,
            ValueError(
                f"{name}:{_INDEXERS.get(name, None)} "
                "is already registered as a KNNIndexer"
            ),
        )
        setattr(cls, _INDEXER_ATTR, name)
        _INDEXERS[name] = cls
        return cls

    return deco


@fugue_ml_plugin
def knn_indexer(indexer: Any, **kwargs: Any) -> "KNNIndexer":
    if isinstance(indexer, str):
        # knn_indexer as plugin has loaded all entry points
        return _INDEXERS[indexer](**kwargs)
    elif isinstance(indexer, KNNIndexer):
        return indexer
    elif isinstance(indexer, type) and issubclass(indexer, KNNIndexer):
        return indexer(**kwargs)
    else:
        raise ValueError(f"{indexer} is not a valid KNNIndexer")


class KNNIndexer(ABC):
    def __init__(self, metric: str):
        self.metric = metric

    @abstractmethod  # pragma: no cover
    def build(self, index: AnyDataFrame, vec_col: str, **kwargs: Any) -> "KNNIndexer":
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def search_local(
        self,
        queries: np.ndarray,
        k: int,
        **kwargs: Any,
    ) -> Tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def can_broadcast(self, size_limit: int) -> bool:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def get_metadata_df(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def get_metadata_schema(self) -> Schema:
        raise NotImplementedError

    def save(self, path: str) -> None:
        with zip_temp(path) as tmpdir:
            fs, path = fsspec.core.url_to_fs(tmpdir)
            fs.write_bytes(
                os.path.join(path, "indexer_type.bin"), pickle.dumps(self.__class__)
            )
            params = dict(self.__dict__)
            self.save_special_params(params, tmpdir)
            fs.write_bytes(os.path.join(path, "params.bin"), pickle.dumps(params))

    @staticmethod
    def load(path: str, cache_size: Any = None) -> "KNNIndexer":
        return _INDEXER_LOADER.load(path, cache_size=cache_size)

    def save_special_params(self, data: Dict[str, Any], folder: str) -> None:
        return

    def load_special_params(self, folder: str) -> Dict[str, Any]:
        return {}

    def search(
        self,
        queries: AnyDataFrame,
        k: int,
        vec_col: str,
        dist_col: Optional[str] = None,
        rank_col: Optional[str] = None,
        index_cache_mem_limit: Any = "1g",
        queries_chunk_mem_limit: Any = "100m",
        queries_chunk_row_limit: int = 0,
        broadcast_limit: Any = "500m",
        drop_vec_col: bool = True,
        temp_file: Optional[str] = None,
        index_replicates: Optional[int] = None,
        **kwargs: Any,
    ) -> AnyDataFrame:
        output_schema = self._construct_schema(
            fa.get_schema(queries),
            vec_col=vec_col,
            dist_col=dist_col,
            rank_col=rank_col,
            drop_vec_col=drop_vec_col,
        )
        indexer_ser = _KNNIndexerSerializer(self, to_size(broadcast_limit), temp_file)

        def _wrapper(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
            indexer = indexer_ser.get_instance(cache_size=index_cache_mem_limit)
            reslicer = PandasBatchReslicer(
                row_limit=queries_chunk_row_limit, size_limit=queries_chunk_mem_limit
            )
            for df in reslicer.reslice(dfs):
                for res in _search_pd_df(
                    indexer=indexer,
                    df=df,
                    k=k,
                    vec_col=vec_col,
                    dist_col=dist_col,
                    rank_col=rank_col,
                    drop_vec_col=drop_vec_col,
                    **kwargs,
                ):
                    yield res[output_schema.names]

        return fa.transform(
            queries, _wrapper, schema=output_schema, partition=index_replicates
        )

    def get_np_arr(self, df: pd.DataFrame, vec_col: str) -> np.array:
        return np.array(list(df[vec_col]))

    def _construct_schema(
        self,
        schema: Schema,
        vec_col: str,
        dist_col: Optional[str],
        rank_col: Optional[str],
        drop_vec_col: bool,
    ) -> Schema:
        schema = schema + self.get_metadata_schema()
        assert_or_throw(
            is_vec_col(schema, vec_col), ValueError(f"{vec_col} is not a vector column")
        )
        if dist_col is not None:
            schema = schema + (dist_col, float)
        if rank_col is not None:
            schema = schema + (rank_col, int)
        if drop_vec_col:
            schema = schema.exclude(vec_col)
        return schema


class KNNLocalIndexer(KNNIndexer):
    def build(self, index: AnyDataFrame, vec_col: str, **kwargs: Any) -> "KNNIndexer":
        pdf = fa.as_pandas(index).reset_index(drop=True)
        self._metadata_df = pdf.drop(columns=[vec_col])
        self._metadata_schema = fa.get_schema(index) - vec_col
        self.build_local(self.get_np_arr(pdf, vec_col=vec_col), **kwargs)
        return self

    def get_metadata_df(self) -> pd.DataFrame:
        return self._metadata_df

    def get_metadata_schema(self) -> Schema:
        return self._metadata_schema

    @abstractmethod  # pragma: no cover
    def build_local(self, arr: np.ndarray, **kwargs: Any) -> None:
        raise NotImplementedError


class KNNShardingIndexer(KNNIndexer):
    def __init__(
        self,
        metric: str,
        indexer: Any,
        group_cols: Optional[List[str]] = None,
        index_shards: Optional[int] = None,
        broadcast_limit: Any = "10m",
        save_dir: Optional[str] = None,
        indexer_init_kwargs: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(metric)

        self._internal_group_cols: List[str] = []
        if group_cols is not None:
            self._internal_group_cols += group_cols
            self._group_cols = group_cols
        else:
            self._group_cols = []
        if index_shards is not None and index_shards > 1:
            self._internal_group_cols += [_INDEXER_SHARD_COLUMN_NAME]
            self._index_shards = index_shards
        else:
            self._index_shards = 1
        assert_or_throw(
            len(self._internal_group_cols) > 0,
            ValueError("neither group_cols contains columns nor index_shards>1)"),
        )

        self._indexer = indexer
        self._broadcast_limit = to_size(broadcast_limit)
        self._save_dir = save_dir
        self._indexer_init_kwargs = indexer_init_kwargs or {}

    def build(self, index: AnyDataFrame, vec_col: str, **kwargs: Any) -> "KNNIndexer":
        index = fa.as_fugue_df(index)
        if self._index_shards > 1:
            index = deterministic_shard(
                index,
                self._index_shards,
                _INDEXER_SHARD_COLUMN_NAME,
                from_cols=[x for x in fa.get_column_names(index) if x != vec_col],
            )

        input_schema = fa.get_schema(index)
        assert_or_throw(
            is_vec_col(input_schema, vec_col),
            ValueError(f"{vec_col} is not a vector column"),
        )
        output_schema = input_schema.extract(self._internal_group_cols) + (
            _INDEXER_BLOB_COLUMN_NAME,
            bytes,
        )

        def _build_group(df: pd.DataFrame) -> pd.DataFrame:
            indexer = knn_indexer(
                self._indexer, metric=self.metric, **self._indexer_init_kwargs
            )
            subdf = df.drop(columns=self._internal_group_cols)
            indexer.build(subdf, vec_col=vec_col, **kwargs)
            if self._save_dir is not None:
                temp_file: Optional[str] = os.path.join(
                    self._save_dir, str(uuid4()) + ".bin"
                )
            else:
                temp_file = None
            ser = _KNNIndexerSerializer(
                indexer, self._broadcast_limit, temp_file=temp_file
            )
            return df.head(1)[self._internal_group_cols].assign(
                **{_INDEXER_BLOB_COLUMN_NAME: pickle.dumps(ser)}
            )[output_schema.names]

        self._index = fa.as_pandas(
            fa.transform(
                index,
                _build_group,
                schema=output_schema,
                partition=self._internal_group_cols,
            ),
        )
        self._mem_size = int(self._index.memory_usage(deep=True).sum())
        example = pickle.loads(self._index.iloc[0, -1])
        self._metadata_schema = example.metadata_schema
        return self

    def search_local(
        self, queries: np.ndarray, k: int, **kwargs: Any
    ) -> Tuple[np.ndarray, np.ndarray]:  # pragma: no cover
        raise NotImplementedError(
            "search_local is not supported for KNNShardingIndexer"
        )

    def can_broadcast(self, size_limit: int) -> bool:
        return self._mem_size < size_limit

    def get_metadata_df(self) -> pd.DataFrame:  # pragma: no cover
        raise NotImplementedError

    def get_metadata_schema(self) -> Schema:
        return self._metadata_schema

    def search(  # noqa: C901
        self,
        queries: AnyDataFrame,
        k: int,
        vec_col: str,
        dist_col: Optional[str] = None,
        rank_col: Optional[str] = None,
        index_cache_mem_limit: Any = "1g",
        queries_chunk_mem_limit: Any = "100m",
        queries_chunk_row_limit: int = 0,
        broadcast_limit: Any = "500m",
        drop_vec_col: bool = True,
        temp_file: Optional[str] = None,
        index_replicates: Optional[int] = None,
        **kwargs: Any,
    ) -> AnyDataFrame:

        assert_or_throw(
            rank_col is None or self._index_shards <= 1,
            NotImplementedError("rank_col is not supported when index_shards>1"),
        )

        is_dist_temp = False
        if self._index_shards > 1 and dist_col is None:
            # when index is sharded, we must keep a dist_col
            # so that we can merge the results from different shards
            dist_col = _TEMP_DIST_COL
            is_dist_temp = True

        queries_schema = fa.get_schema(queries)

        output_schema = self._construct_schema(
            queries_schema,
            vec_col=vec_col,
            dist_col=dist_col,
            rank_col=rank_col,
            drop_vec_col=drop_vec_col,
        )
        indexer_ser = _KNNIndexerSerializer(self, to_size(broadcast_limit), temp_file)
        group_cols = self._internal_group_cols
        sharded = False

        if index_replicates is not None and index_replicates > 1:
            if self._index_shards > 1:
                queries = deterministic_shard_and_replicate(
                    queries,
                    index_replicates,
                    _INDEXER_REPLICATES_COLUMN_NAME,
                    from_cols=[x for x in fa.get_column_names(queries) if x != vec_col],
                    replicates=self._index_shards,
                    replicate_col=_INDEXER_SHARD_COLUMN_NAME,
                )
            else:
                queries = deterministic_shard(
                    queries,
                    index_replicates,
                    _INDEXER_REPLICATES_COLUMN_NAME,
                    from_cols=[x for x in fa.get_column_names(queries) if x != vec_col],
                )
            sharded = True
        elif self._index_shards > 1:
            queries = replicate(queries, self._index_shards, _INDEXER_SHARD_COLUMN_NAME)

        def _wrapper(df: pd.DataFrame) -> Iterable[pd.DataFrame]:
            if sharded:
                df = df.drop(columns=[_INDEXER_REPLICATES_COLUMN_NAME])
            g_indexer = indexer_ser.get_instance(cache_size=index_cache_mem_limit)
            has_return = False
            idx = g_indexer._index.merge(df.head(1)[group_cols])  # type: ignore
            if len(idx) > 0:  # found the corresponding group
                indexer = pickle.loads(idx.iloc[0, -1]).get_instance(
                    cache_size=index_cache_mem_limit
                )
                reslicer = PandasBatchReslicer(
                    row_limit=queries_chunk_row_limit,
                    size_limit=queries_chunk_mem_limit,
                )
                for subdf in reslicer.reslice([df]):
                    for res in _search_pd_df(
                        indexer=indexer,
                        df=subdf,
                        k=k,
                        vec_col=vec_col,
                        dist_col=dist_col,
                        rank_col=rank_col,
                        drop_vec_col=drop_vec_col,
                        **kwargs,
                    ):
                        if len(res) > 0:
                            has_return = True
                            yield res[output_schema.names]
            if not has_return:  # TODO: this is a hack, need to fix Fugue
                yield pd.DataFrame(columns=output_schema.names)

        res = fa.transform(
            queries,
            _wrapper,
            schema=output_schema,
            partition=group_cols
            if not sharded
            else group_cols + [_INDEXER_REPLICATES_COLUMN_NAME],
        )

        if self._index_shards > 1:
            res = fa.take(
                res,
                n=k,
                presort=dist_col,
                partition=queries_schema.exclude(vec_col).names,
            )

        if is_dist_temp:
            res = fa.drop_columns(res, [dist_col])

        return res


class _KNNIndexerSerializer:
    def __init__(
        self,
        indexer: KNNIndexer,
        broadcast_size_limit: int,
        temp_file: Optional[str] = None,
    ):
        if indexer.can_broadcast(broadcast_size_limit):
            self._indexer_obj: Union[KNNIndexer, str] = indexer
        else:
            assert_or_throw(temp_file is not None, ValueError("temp_file is required"))
            indexer.save(temp_file)  # type: ignore
            self._indexer_obj = temp_file  # type: ignore
            # Because of lazy evaluation, this class should not delete the temp file
        self.metadata_schema = indexer.get_metadata_schema()

    def get_instance(self, cache_size: Any) -> KNNIndexer:
        if isinstance(self._indexer_obj, str):
            return KNNIndexer.load(self._indexer_obj, cache_size=cache_size)
        else:
            return self._indexer_obj


class _KNNIndexerLoader:
    def __init__(self):
        self._reset()

    def __setstate__(self, state: Any) -> None:
        self._reset()

    def __getstate__(self) -> Any:
        return {}

    def get_cache_items(self) -> List[KNNIndexer]:
        return [self._indexers[tp[2]] for tp in self._hits]

    def load(self, path: str, cache_size: Any) -> KNNIndexer:
        limit = to_size(cache_size) if cache_size is not None else 0
        with self._lock:
            if path not in self._indexers:
                indexer, size = self._load(path)
                if size > limit:
                    return indexer
                self._indexers[path] = indexer
                self._n += 1
                self._hits.append((1, self._n, path, size))
                self._update_cache(limit)
                return indexer
            else:
                indexer = self._indexers[path]
                for i in range(len(self._hits)):
                    if self._hits[i][2] == path:
                        self._n += 1
                        self._hits[i] = (
                            self._hits[i][0] + 1,
                            self._n,
                            self._hits[i][2],
                            self._hits[i][3],
                        )
                        self._update_cache(limit)
                        break
                return indexer

    def _reset(self):
        self._lock = SerializableRLock()
        self._indexers: Dict[str, KNNIndexer] = {}
        self._hits: List[Tuple[int, int, str, int]] = []
        self._n = 0

    def _update_cache(self, limit: int) -> None:
        total = sum(x[-1] for x in self._hits)
        self._hits.sort(reverse=True)
        while total > limit:
            tp = self._hits.pop()
            del self._indexers[tp[2]]
            total -= tp[-1]

    def _load(self, path: str) -> Tuple[KNNIndexer, int]:
        with unzip_to_temp(path) as tmpdir:
            fs, path = fsspec.core.url_to_fs(tmpdir)
            blob = fs.read_bytes(os.path.join(path, "indexer_type.bin"))
            tp = pickle.loads(blob)
            params_blob = fs.read_bytes(os.path.join(path, "params.bin"))
            params = pickle.loads(params_blob)
            indexer = tp.__new__(tp)
            indexer.__dict__.update(params)
            indexer.__dict__.update(indexer.load_special_params(tmpdir))
            return indexer, len(blob) + len(params_blob)


_INDEXER_LOADER = _KNNIndexerLoader()


def _search_pd_df(
    indexer: KNNIndexer,
    df: pd.DataFrame,
    k: int,
    vec_col: str,
    dist_col: Optional[str],
    rank_col: Optional[str],
    drop_vec_col: bool,
    **kwargs: Any,
) -> Iterable[pd.DataFrame]:
    qarr = indexer.get_np_arr(df, vec_col=vec_col)
    idx, dist = indexer.search_local(qarr, k=k, **kwargs)
    del qarr
    df = df.reset_index(drop=True)
    if drop_vec_col:
        df = df.drop(columns=[vec_col])
    for j in range(min(k, idx.shape[1])):
        meta = indexer.get_metadata_df().iloc[idx[:, j]].reset_index(drop=True)
        more_cols: Dict[str, Any] = {}
        if dist_col is not None:
            more_cols[dist_col] = dist[:, j]
        if rank_col is not None:
            more_cols[rank_col] = j
        if len(more_cols) > 0:
            df = df.assign(**more_cols)
        yield pd.concat([df, meta], axis=1)
