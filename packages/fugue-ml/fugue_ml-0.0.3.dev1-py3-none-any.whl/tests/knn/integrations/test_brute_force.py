import fugue.api as fa
import numpy as np
import pandas as pd
from pytest import fixture, raises

from fugue_ml.knn import KNNIndexer
from fugue_ml.knn.brute_force import BruteForceKNNIndexer


@fixture
def indexer(tmpdir):
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = arr1 + 0.001
    arr = np.concatenate([arr1, arr2], axis=0)
    index = pd.DataFrame(dict(idx=range(len(arr)), dummy=10, vec_x=list(arr)))
    bi = BruteForceKNNIndexer(metric="cos").build(index, vec_col="vec_x")
    path = str(tmpdir.join("index.bin"))
    bi.save(path)
    return KNNIndexer.load(path)


@fixture
def queries():
    arr1 = np.array([[1, 2], [3, 4]])
    arr3 = arr1 - 0.001
    arr = np.concatenate([arr1, arr3], axis=0)
    return pd.DataFrame(dict(q=range(len(arr)), vec=list(arr)))


def test_search(indexer, queries, tmpdir):
    with raises(KeyError):
        indexer.search(queries, 1, vec_col="vec1")

    with raises(ValueError):
        indexer.search(queries, 1, vec_col="idx")

    res = fa.as_pandas(
        indexer.search(
            queries,
            1,
            vec_col="vec",
            queries_chunk_mem_limit=1,
            broadcast_limit=1,
            temp_file=str(tmpdir.join("temp.bin")),
        )
    )
    actual = set(tuple(x) for x in res[["q", "idx", "dummy"]].values.tolist())
    assert actual == {(0, 0, 10), (1, 1, 10), (2, 0, 10), (3, 1, 10)}

    res = fa.as_pandas(indexer.search(queries, 1, vec_col="vec", dist_col="dist"))
    actual = set(
        tuple(int(xx) for xx in x)
        for x in res[["q", "idx", "dummy", "dist"]].values.tolist()
    )
    assert actual == {(0, 0, 10, 0), (1, 1, 10, 0), (2, 0, 10, 0), (3, 1, 10, 0)}
