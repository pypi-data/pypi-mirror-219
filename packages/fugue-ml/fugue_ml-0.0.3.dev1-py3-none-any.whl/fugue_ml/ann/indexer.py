from typing import Any, Iterable, Optional, Dict

import numpy as np
import pandas as pd
from fugue import AnyDataFrame
import fugue.api as fa
import gc
from triad import Schema


class ANNIndexer:
    def __init__(
        self,
        metric: str,
        vec_col: str = "vector",
        init_params: Optional[Dict[str, Any]] = None,
        build_params: Optional[Dict[str, Any]] = None,
        search_params: Optional[Dict[str, Any]] = None,
    ):
        self.metric = metric
        self.init_params = init_params or {}
        self.build_params = build_params or {}
        self.search_params = search_params or {}
        self.vec_col = vec_col
        self.local_index_df: Optional[pd.DataFrame] = None
        self.local_index_schema: Optional[Schema] = None

    def build(self, df: AnyDataFrame, **kwargs: Any) -> "ANNIndexer":
        raise NotImplementedError

    def search_index_local(
        self,
        df: pd.DataFrame,
        top_n: int,
        idx_col: str,
        dist_col: Optional[str],
        remove_vec_col: bool,
        **kwargs: Any,
    ) -> pd.DataFrame:
        raise NotImplementedError

    def search_local(
        self,
        df: pd.DataFrame,
        top_n: int,
        dist_col: Optional[str],
        remove_vec_col: bool,
        **kwargs: Any,
    ) -> pd.DataFrame:
        tdf = self.search_index_local(
            df,
            top_n,
            idx_col="__temp_idx",
            dist_col=dist_col,
            remove_vec_col=remove_vec_col,
            **kwargs,
        )
        tdf = tdf.explode(
            "__temp_idx" if dist_col is None else ["__temp_idx", dist_col]
        )
        tdf = tdf.merge(self.local_index_df, left_on="__temp_idx", right_index=True)
        tdf = tdf.drop(columns=["__temp_idx"])
        return tdf

    def search_index(
        self,
        df: AnyDataFrame,
        top_n: int,
        idx_col: str = "idx",
        dist_col: Optional[str] = None,
        remove_vec_col: bool = True,
        **kwargs: Any,
    ) -> AnyDataFrame:
        schema = self._construct_schema(
            fa.get_schema(df), idx_col, dist_col, remove_vec_col
        )
        params = {**self.search_params, **kwargs}

        def _wrapper(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
            for df in dfs:
                yield self.search_index_local(
                    df,
                    top_n,
                    idx_col=idx_col,
                    dist_col=dist_col,
                    remove_vec_col=remove_vec_col,
                    **params,
                )[schema.names]
                gc.collect()

        return fa.transform(df, _wrapper, schema=schema)

    def search(
        self,
        df: AnyDataFrame,
        top_n: int,
        dist_col: Optional[str] = None,
        remove_vec_col: bool = True,
        **kwargs: Any,
    ) -> AnyDataFrame:
        schema = self._construct_schema(
            fa.get_schema(df), None, dist_col, remove_vec_col
        )

        def _wrapper(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
            for df in dfs:
                yield self.search_local(
                    df,
                    top_n,
                    dist_col=dist_col,
                    remove_vec_col=remove_vec_col,
                    **kwargs,
                )[schema.names]
                gc.collect()

        return fa.transform(df, _wrapper, schema=schema)

    def get_np_arr(self, df: pd.DataFrame) -> np.array:
        return np.array(list(df[self.vec_col]))

    def _construct_schema(
        self,
        schema: Schema,
        idx_col: Optional[str],
        dist_col: Optional[str],
        remove_vec_col: bool,
    ) -> Schema:
        if idx_col is not None:
            schema = schema + (idx_col, [int])
            if dist_col is not None:
                schema = schema + (dist_col, [float])
        else:
            schema = schema + self.local_index_schema
            if dist_col is not None:
                schema = schema + (dist_col, float)
        if remove_vec_col:
            schema = schema.exclude(self.vec_col)
        return schema


class ANNLocalIndexer(ANNIndexer):
    def build(self, df: AnyDataFrame, **kwargs: Any) -> "ANNIndexer":
        params = {**self.build_params, **kwargs}
        pdf = fa.as_pandas(df).reset_index(drop=True)
        self.local_index_df = pdf.drop(columns=[self.vec_col])
        self.local_index_schema = fa.get_schema(df) - self.vec_col
        return self.build_local(self.get_np_arr(pdf), **params)

    def build_local(self, arr: np.ndarray, **kwargs: Any) -> "ANNLocalIndexer":
        raise NotImplementedError
