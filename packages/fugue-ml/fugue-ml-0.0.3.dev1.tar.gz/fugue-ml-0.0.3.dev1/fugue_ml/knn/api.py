import os
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

import fugue.api as fa
from fugue import AnyDataFrame
from triad import assert_or_throw

from fugue_ml.utils.schema import is_vec_col

from .indexer import KNNShardingIndexer, knn_indexer
from .brute_force import BruteForceKNNIndexer


def compute_knn(
    index: AnyDataFrame,
    queries: AnyDataFrame,
    k: int = 1,
    vec_col: str = "vector",
    partition: Union[str, List[str], None] = None,
    indexer: Any = BruteForceKNNIndexer,
    metric: str = "cos",
    dist_col: Optional[str] = None,
    rank_col: Optional[str] = None,
    drop_vec_col: bool = True,
    index_cache_mem_limit: Any = "1g",
    queries_chunk_mem_limit: Any = "100m",
    queries_chunk_row_limit: int = 0,
    broadcast_limit: Any = "100m",
    temp_path: Optional[str] = None,
    index_replicates: Optional[int] = None,
    index_shards: Optional[int] = None,
    init_kwargs: Optional[Dict[str, Any]] = None,
    build_kwargs: Optional[Dict[str, Any]] = None,
    search_kwargs: Optional[Dict[str, Any]] = None,
) -> AnyDataFrame:
    """Compute the k nearest neighbors of queries in index

    :param index: the index dataframe
    :param queries: the query dataframe
    :param k: number of nearest neighbors
    :param vec_col: the column name of the vector column
    :param partition: partition keys, default to None (no hard partitioning)
    :param indexer: indexer name, default to brute_force
    :param metric: distance metric, default to cos
    :param dist_col: the column name of the distance column, default to None
        (no distance column)
    :param rank_col: the column name of the rank column, default to None
        (no rank column)
    :param drop_vec_col: whether to drop the vector column in the output,
        default to True
    :param index_cache_mem_limit: the memory constraint on index cache
        in worker memory, default to 1g
    :param queries_chunk_mem_limit: the memory constraint on queries chunks,
        default to 100m
    :param queries_chunk_row_limit: the row constraint on queries chunks,
        default to 0 (no row constraint)
    :param broadcast_limit: the memory constraint when broadcasting the index,
    :param temp_path: the temp directory to store intermediate data, default to None
    :param index_replicates: number of index replicates, default to None. For example,
        if index_replicates=2, there will be 2 identical indexers processing different
        portions of the data. This is to increase parallelism for large queries.
    :param index_shards: number of index shards, default to None. For example, if
        index_shards=2, the index will be partitioned into 2 shards. This is to
        improve parallelism for large index.
    :return: the index dataframe with search results from index
    """
    index_schema = fa.get_schema(index)
    assert_or_throw(
        is_vec_col(index_schema, vec_col),
        ValueError(f"{vec_col} is not a vector column in index"),
    )
    queries_schema = fa.get_schema(queries)
    assert_or_throw(
        is_vec_col(queries_schema, vec_col),
        ValueError(f"{vec_col} is not a vector column in queries"),
    )
    if temp_path is None:
        temp_file: Optional[str] = None
    else:
        temp_file = os.path.join(temp_path, str(uuid4()) + ".bin")
    if partition is None and index_shards is None:
        idx = knn_indexer(indexer, metric=metric, **(init_kwargs or {}))
    else:
        by = [partition] if isinstance(partition, str) else partition
        idx = KNNShardingIndexer(
            metric=metric,
            indexer=indexer,
            group_cols=by,
            index_shards=index_shards,
            broadcast_limit=broadcast_limit,
            save_dir=temp_path,
            indexer_init_kwargs=init_kwargs,
        )
    idx.build(index, vec_col=vec_col, **(build_kwargs or {}))
    return idx.search(
        queries,
        k=k,
        vec_col=vec_col,
        dist_col=dist_col,
        rank_col=rank_col,
        index_cache_mem_limit=index_cache_mem_limit,
        queries_chunk_mem_limit=queries_chunk_mem_limit,
        queries_chunk_row_limit=queries_chunk_row_limit,
        broadcast_limit=broadcast_limit,
        drop_vec_col=drop_vec_col,
        temp_file=temp_file,
        index_replicates=index_replicates,
        **(search_kwargs or {}),
    )
