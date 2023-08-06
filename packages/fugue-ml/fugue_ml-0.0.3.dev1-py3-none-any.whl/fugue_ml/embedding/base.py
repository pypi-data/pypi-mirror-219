import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, Optional, Tuple

import fugue.api as fa
import fugue.column as fc
import pandas as pd
import pyarrow as pa
from fugue import AnyDataFrame, PartitionSpec
from triad import Schema, assert_or_throw
from triad.utils.batch_reslicers import PandasBatchReslicer

from fugue_ml.utils.params import merge_dicts
from fugue_ml.utils.registry import fugue_ml_plugin
from fugue_ml.utils.schema import is_vec_col

from .cache import _EMBEDDING_CACHE_UID, EmbeddingCache


@fugue_ml_plugin
def parse_embedding_model(model: Any, **kwargs: Any) -> "Embedding":
    if isinstance(model, Embedding):
        return model
    if isinstance(model, type) and issubclass(model, Embedding):
        return model(**kwargs)
    raise ValueError(f"unrecognized embedding model {model}")


class Embedding(ABC):
    def __init__(
        self,
        model_params: Optional[Dict[str, Any]] = None,
        tokenizing_params: Optional[Dict[str, Any]] = None,
        encoding_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__()
        self.model_params = model_params or {}
        self.tokenizing_params = tokenizing_params or {}
        self.encoding_params = encoding_params or {}

    @property
    def token_size_range(self) -> Tuple[int, int]:  # pragma: no cover
        return 1, sys.maxsize

    @abstractmethod  # pragma: no cover
    def encode_local(
        self,
        df: pd.DataFrame,
        col: str,
        vec_col: str,
        vec_type: pa.DataType,
        **kwargs: Any,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def count_input_tokens_local(
        self,
        df: pd.DataFrame,
        col: str,
        token_col: str,
        **kwargs: Any,
    ) -> pd.DataFrame:
        raise NotImplementedError

    def encode(
        self,
        df: AnyDataFrame,
        col: str,
        vec_col: Any,
        batch_rows: int = 0,
        token_size_range: Optional[Tuple[int, int]] = None,
        on_invalid_token_size: str = "raise",
        tokenizing_params: Optional[Dict[str, Any]] = None,
        cache: Optional["EmbeddingCache"] = None,
        cache_uid_col: str = _EMBEDDING_CACHE_UID,
        **kwargs: Any,
    ) -> AnyDataFrame:
        _validate_on_invalid_token_size(on_invalid_token_size)
        input_schema = fa.get_schema(df)
        if fa.is_local(df):
            df = fa.repartition(df, fa.get_current_parallelism() * 2)
        token_size_range = token_size_range or self.token_size_range
        assert_or_throw(
            col in input_schema,
            ValueError(f"column {col} not found in input dataframe {input_schema}"),
        )
        try:
            embedding_schema = Schema(vec_col)
            vec_col_name = embedding_schema.names[0]
        except Exception as e:
            raise ValueError(
                f"invalid embedding vec_col {vec_col}, it must be a schema expression"
            ) from e

        assert_or_throw(
            len(embedding_schema) == 1 and is_vec_col(embedding_schema, vec_col_name),
            ValueError(
                f"embedding column must have only one vector column {embedding_schema}"
            ),
        )
        output_schema = input_schema + embedding_schema

        if cache is not None:
            cached, df = cache.query(df, uid_col=cache_uid_col, vec_col=vec_col_name)
            if df is None:  # all found in cache
                return cached

        params = merge_dicts(
            self.encoding_params,
            kwargs,
            {
                "col": col,
                "vec_col": embedding_schema.names[0],
                "vec_type": embedding_schema.types[0].value_type,
                "batch_rows": batch_rows,
                "token_size_range": token_size_range,
                "on_invalid_token_size": on_invalid_token_size,
                "tokenizing_params": merge_dicts(
                    self.tokenizing_params, tokenizing_params
                ),
            },
        )

        df = fa.transform(
            df,
            self._encode_stream,
            schema=output_schema,
            params=params,
        )

        if cache is not None:
            df = fa.persist(df)
            cache.upsert(df, uid_col=cache_uid_col, vec_col=vec_col_name)
            if cached is not None:
                return fa.union(cached, df, distinct=False)

        return df

    def count_input_tokens(
        self,
        df: AnyDataFrame,
        col: str,
        token_col: Optional[str] = None,
        token_size_range: Optional[Tuple[int, int]] = None,
        on_invalid_token_size: str = "raise",
        partition: Any = None,
        summarize: bool = False,
        cache: Optional["EmbeddingCache"] = None,
        cache_uid_col: str = _EMBEDDING_CACHE_UID,
        **kwargs: Any,
    ) -> AnyDataFrame:
        _validate_on_invalid_token_size(on_invalid_token_size)
        token_col = token_col or col + "_token_count"
        token_size_range = token_size_range or self.token_size_range
        if not summarize:
            input_schema = fa.get_schema(df)
            if fa.is_local(df):
                df = fa.repartition(df, fa.get_current_parallelism() * 2)
            output_schema = input_schema + (token_col, int)
            params = merge_dicts(
                self.tokenizing_params,
                kwargs,
                {
                    "col": col,
                    "token_col": token_col,
                    "token_size_range": token_size_range,
                    "on_invalid_token_size": on_invalid_token_size,
                },
            )

            return fa.transform(
                df,
                self._count_input_tokens_stream,
                schema=output_schema,
                params=params,
            )
        else:
            ps = PartitionSpec(partition)

            if cache is not None:
                df = cache.find_new(df, uid_col=cache_uid_col)

            subdf = fa.select_columns(df, ps.partition_by + [col])
            token_col = col + "_token_count"
            res = self.count_input_tokens(
                subdf,
                col=col,
                token_col=token_col,
                token_size_range=token_size_range,
                on_invalid_token_size=on_invalid_token_size,
                summarize=False,
                **kwargs,
            )
            res = fa.persist(fa.select_columns(res, ps.partition_by + [token_col]))
            if not fa.is_empty(res):
                return fa.select(
                    res,
                    *[fc.col(x) for x in ps.partition_by],
                    fc.functions.sum(fc.col(token_col)),
                    fc.functions.count(fc.all_cols()).alias(col + "_row_count"),
                )
            return pd.DataFrame({token_col: [0], col + "_row_count": [0]})

    def _count_input_tokens_stream(
        self,
        dfs: Iterable[pd.DataFrame],
        col: str,
        token_col: str,
        token_size_range: Tuple[int, int],
        on_invalid_token_size: str,
        **kwargs: Any,
    ) -> Iterable[pd.DataFrame]:
        for df in dfs:
            orig = self.count_input_tokens_local(
                df, col=col, token_col=token_col, **kwargs
            )
            res = orig[orig[token_col].between(*token_size_range, inclusive="both")]
            if len(res) < len(orig):
                if on_invalid_token_size == "raise":
                    raise ValueError(
                        f"input column {col} has values "
                        f"out of token size range {token_size_range}"
                    )
                elif on_invalid_token_size == "skip":
                    pass
                else:  # pragma: no cover
                    raise ValueError(
                        f"invalid on_invalid_token_size option {on_invalid_token_size}"
                    )
            if len(res) >= 0:
                yield res

    def _encode_stream(
        self,
        dfs: Iterable[pd.DataFrame],
        col: str,
        vec_col: str,
        vec_type: pa.DataType,
        batch_rows: int,
        token_size_range: Tuple[int, int],
        on_invalid_token_size: str,
        tokenizing_params: Dict[str, Any],
        **kwargs: Any,
    ) -> Iterable[pd.DataFrame]:
        slicer = PandasBatchReslicer(row_limit=batch_rows)
        token_col = col + "_token_count_temp"
        tdfs = self._count_input_tokens_stream(
            dfs,
            col=col,
            token_col=token_col,
            token_size_range=token_size_range,
            on_invalid_token_size=on_invalid_token_size,
            **tokenizing_params,
        )
        for df in slicer.reslice(tdfs):
            yield self.encode_local(
                df.drop(columns=[token_col]),
                col=col,
                vec_col=vec_col,
                vec_type=vec_type,
                **kwargs,
            )


def _validate_on_invalid_token_size(on_invalid_token_size: str) -> None:
    if on_invalid_token_size not in ["raise", "skip"]:
        raise ValueError(
            f"invalid on_invalid_token_size option {on_invalid_token_size}"
        )
