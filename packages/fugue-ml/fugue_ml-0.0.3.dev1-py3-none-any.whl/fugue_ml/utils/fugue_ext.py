from typing import Any, Iterable, List

import fugue.api as fa
import numpy as np
import pandas as pd
from fugue import AnyDataFrame
from triad import assert_or_throw


def deterministic_shard(
    df: AnyDataFrame,
    num_shards: int,
    shard_col: str,
    from_cols: List[str],
) -> AnyDataFrame:
    """Gererate deterministic shard id based on the given columns

    :param df: input dataframe
    :param num_shards: number of shards
    :param shard_col: the shard column name
    :param from_cols: columns to generate the deterministic shard id
    :return: a dataframe with the deterministic shard id
    """
    assert_or_throw(len(from_cols) > 0, ValueError("from_cols cannot be empty"))
    assert_or_throw(num_shards > 0, ValueError("num_shards must be positive"))

    def _shard(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
        for df in dfs:
            yield df.assign(
                **{
                    shard_col: pd.util.hash_pandas_object(
                        df[from_cols], index=False
                    ).mod(num_shards)
                }
            )

    return fa.transform(df, _shard, schema=fa.get_schema(df) + (shard_col, int))


def random_shard(
    df: AnyDataFrame,
    num_shards: int,
    shard_col: str,
    seed: Any = None,
) -> AnyDataFrame:
    """Gererate rand shard id based on the given columns

    :param df: input dataframe
    :param num_shards: number of shards
    :param shard_col: the shard column name
    :param seed: seed for random number generator on each worker
    :return: a dataframe with the random shard id
    """
    assert_or_throw(num_shards > 0, ValueError("num_shards must be positive"))

    def _shard(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
        if seed is not None:
            np.random.seed(seed)
        for df in dfs:
            yield df.assign(
                **{
                    shard_col: np.random.randint(0, num_shards, size=len(df)),
                }
            )

    return fa.transform(df, _shard, schema=fa.get_schema(df) + (shard_col, int))


def replicate(df: AnyDataFrame, n: int, replicate_col: str) -> AnyDataFrame:
    """Replicate the dataframe n times

    :param df: input dataframe
    :param n: number of replications
    :param replicate_col: the column name of the replication id
    :return: a dataframe with the replication id
    """
    assert_or_throw(n > 0, ValueError("n must be positive"))

    def _replicate(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
        # TODO: is pa.Table a better choice?
        for df in dfs:
            for k in range(n):
                yield df.assign(**{replicate_col: k})

    return fa.transform(df, _replicate, schema=fa.get_schema(df) + (replicate_col, int))


def deterministic_shard_and_replicate(
    df: AnyDataFrame,
    num_shards: int,
    shard_col: str,
    from_cols: List[str],
    replicates: int,
    replicate_col: str,
) -> AnyDataFrame:
    """Gererate deterministic shard id based on the given columns and replicate n times

    :param df: input dataframe
    :param num_shards: number of shards
    :param shard_col: the shard column name
    :param from_cols: columns to generate the deterministic shard id
    :param replicates: number of replications
    :param replicate_col: the column name of the replication id
    :return: a dataframe with the deterministic shard id
    """
    assert_or_throw(len(from_cols) > 0, ValueError("from_cols cannot be empty"))
    assert_or_throw(num_shards > 0, ValueError("num_shards must be positive"))
    assert_or_throw(replicates > 0, ValueError("n must be positive"))

    def _shard(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
        for df in dfs:
            tdf = df.assign(
                **{
                    shard_col: pd.util.hash_pandas_object(
                        df[from_cols], index=False
                    ).mod(num_shards)
                }
            )
            for k in range(replicates):
                yield tdf.assign(**{replicate_col: k})

    return fa.transform(
        df, _shard, schema=fa.get_schema(df) + [(shard_col, int), (replicate_col, int)]
    )
