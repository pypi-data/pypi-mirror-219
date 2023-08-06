from typing import Iterable, Optional, List, Any
import pandas as pd


def slice_df_by_size_col(
    df: pd.DataFrame,
    size_col: str,
    size_limit: int,
    row_limit: Optional[int] = None,
    ignore_oversize: bool = False,
) -> Iterable[pd.DataFrame]:
    for idx in slice_iter_by_size(
        range(len(df)),
        df[size_col],
        size_limit=size_limit,
        row_limit=row_limit,
        ignore_oversize=ignore_oversize,
    ):
        yield df.iloc[idx]


def slice_iter_by_size(
    data: Iterable[Any],
    sizes: Iterable[int],
    size_limit: int,
    row_limit: Optional[int] = None,
    ignore_oversize: bool = False,
) -> Iterable[List[Any]]:
    cache: List[Any] = []
    current_size = 0
    for item, size in zip(data, sizes):
        if size > size_limit:
            if not ignore_oversize:
                raise ValueError(f"size {size} exceeds size limit {size_limit}")
        else:
            if current_size + size > size_limit:
                yield cache
                cache = []
                current_size = 0
            cache.append(item)
            current_size += size
        if row_limit is not None and len(cache) >= row_limit:
            yield cache
            cache = []
            current_size = 0
    if len(cache) > 0:
        yield cache
