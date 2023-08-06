import pickle

import fugue.api as fa
import numpy as np
import pandas as pd
from pytest import fixture, raises
import cloudpickle
from fugue_ml.knn import (
    BruteForceKNNIndexer,
    KNNIndexer,
    KNNShardingIndexer,
    knn_indexer,
)
from fugue_ml.knn.indexer import _KNNIndexerLoader


@fixture
def index_df():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = arr1 + 0.001
    arr = np.concatenate([arr1, arr2], axis=0)
    return pd.DataFrame(dict(idx=range(len(arr)), dummy=10, vec_x=list(arr)))


@fixture
def indexer(index_df, tmpdir):
    bi = BruteForceKNNIndexer(metric="cos").build(index_df, vec_col="vec_x")
    path = str(tmpdir.join("index.bin"))
    bi.save(path)
    return KNNIndexer.load(path)


@fixture
def queries():
    arr1 = np.array([[1, 2], [3, 4]])
    arr3 = arr1 - 0.001
    arr = np.concatenate([arr1, arr3], axis=0)
    return pd.DataFrame(dict(q=range(len(arr)), vec=list(arr)))


def test_init_indexer():
    assert isinstance(knn_indexer("brute_force", metric="l2"), BruteForceKNNIndexer)
    bi = knn_indexer(BruteForceKNNIndexer, metric="cos")
    assert isinstance(bi, BruteForceKNNIndexer)
    assert knn_indexer(bi, metric="l2") is bi
    assert bi.metric == "cos"

    with raises(ValueError):
        knn_indexer(1)


def test_indexer(indexer, queries):
    with raises(KeyError):
        indexer.search(queries, 1, vec_col="vec1")

    with raises(ValueError):
        indexer.search(queries, 1, vec_col="idx")

    res = fa.as_pandas(indexer.search(queries, 1, vec_col="vec"))
    actual = set(tuple(x) for x in res[["q", "idx", "dummy"]].values.tolist())
    assert actual == {(0, 0, 10), (1, 1, 10), (2, 0, 10), (3, 1, 10)}

    res = fa.as_pandas(indexer.search(queries, 1, vec_col="vec", dist_col="dist"))
    actual = set(
        tuple(int(xx) for xx in x)
        for x in res[["q", "idx", "dummy", "dist"]].values.tolist()
    )
    assert actual == {(0, 0, 10, 0), (1, 1, 10, 0), (2, 0, 10, 0), (3, 1, 10, 0)}

    res = fa.as_pandas(indexer.search(queries, 2, vec_col="vec", rank_col="rank"))
    actual = set(tuple(x) for x in res[["q", "idx", "dummy", "rank"]].values.tolist())
    assert actual == {
        (0, 0, 10, 0),
        (1, 1, 10, 0),
        (2, 0, 10, 0),
        (3, 1, 10, 0),
        (0, 2, 10, 1),
        (1, 3, 10, 1),
        (2, 2, 10, 1),
        (3, 3, 10, 1),
    }


def test_sharding_indexer(index_df, queries, tmpdir):
    idf = index_df.assign(g=[0, 0, 1, 1])
    gp = KNNShardingIndexer(metric="cos", indexer=BruteForceKNNIndexer, index_shards=5)

    gp = pickle.loads(pickle.dumps(gp))

    gp.build(idf, vec_col="vec_x")

    path = str(tmpdir.join("index.bin"))
    gp.save(path)
    gp = KNNIndexer.load(path)

    res = fa.as_pandas(gp.search(queries, 1, vec_col="vec"))
    actual = set(tuple(x) for x in res[["q", "idx", "dummy", "g"]].values.tolist())
    assert actual == {
        (0, 0, 10, 0),
        (1, 1, 10, 0),
        (2, 0, 10, 0),
        (3, 1, 10, 0),
    }

    res = fa.as_pandas(gp.search(queries, 1, vec_col="vec", index_replicates=5))
    actual = set(tuple(x) for x in res[["q", "idx", "dummy", "g"]].values.tolist())
    assert actual == {
        (0, 0, 10, 0),
        (1, 1, 10, 0),
        (2, 0, 10, 0),
        (3, 1, 10, 0),
    }


def test_key_grouped_indexer(index_df, queries, tmpdir):
    idf = index_df.assign(g=[0, 0, 1, 1])
    qdf = pd.concat([queries] * 2).assign(g=[1, 1, 1, 2, 0, 2, 2, 2], q=range(8))
    gp = KNNShardingIndexer(
        metric="cos", indexer=BruteForceKNNIndexer, group_cols=["g"]
    )

    gp = pickle.loads(pickle.dumps(gp))

    gp.build(idf, vec_col="vec_x")

    path = str(tmpdir.join("index.bin"))
    gp.save(path)
    gp = KNNIndexer.load(path)
    res = fa.as_pandas(gp.search(qdf, 2, vec_col="vec", rank_col="rank"))
    actual = set(
        tuple(x) for x in res[["q", "g", "idx", "dummy", "rank"]].values.tolist()
    )
    assert actual == {
        (4, 0, 0, 10, 0),
        (4, 0, 1, 10, 1),
        (0, 1, 2, 10, 0),
        (1, 1, 3, 10, 0),
        (2, 1, 2, 10, 0),
        (0, 1, 3, 10, 1),
        (1, 1, 2, 10, 1),
        (2, 1, 3, 10, 1),
    }

    res = fa.as_pandas(
        gp.search(qdf, 2, vec_col="vec", rank_col="rank", index_replicates=5)
    )
    actual = set(
        tuple(x) for x in res[["q", "g", "idx", "dummy", "rank"]].values.tolist()
    )
    assert actual == {
        (4, 0, 0, 10, 0),
        (4, 0, 1, 10, 1),
        (0, 1, 2, 10, 0),
        (1, 1, 3, 10, 0),
        (2, 1, 2, 10, 0),
        (0, 1, 3, 10, 1),
        (1, 1, 2, 10, 1),
        (2, 1, 3, 10, 1),
    }


def test_key_grouped_sharding_indexer(index_df, queries, tmpdir):
    idf = index_df.assign(g=[0, 0, 1, 1])
    qdf = pd.concat([queries] * 2).assign(g=[1, 1, 1, 2, 0, 2, 2, 2], q=range(8))
    gp = KNNShardingIndexer(
        metric="cos", indexer=BruteForceKNNIndexer, group_cols=["g"], index_shards=5
    )

    gp = pickle.loads(pickle.dumps(gp))

    gp.build(idf, vec_col="vec_x")

    path = str(tmpdir.join("index.bin"))
    gp.save(path)
    gp = KNNIndexer.load(path)

    res = fa.as_pandas(gp.search(qdf, 1, vec_col="vec", index_replicates=5))
    actual = set(tuple(x) for x in res[["q", "g", "idx", "dummy"]].values.tolist())
    assert actual == {
        (4, 0, 0, 10),
        (0, 1, 2, 10),
        (1, 1, 3, 10),
        (2, 1, 2, 10),
    }

    res = fa.as_pandas(
        gp.search(qdf, 1, vec_col="vec", dist_col="dist", index_replicates=5)
    )
    assert "dist" in res.columns
    actual = set(tuple(x) for x in res[["q", "g", "idx", "dummy"]].values.tolist())
    assert actual == {
        (4, 0, 0, 10),
        (0, 1, 2, 10),
        (1, 1, 3, 10),
        (2, 1, 2, 10),
    }


def test_indexer_loader():
    class _Loader(_KNNIndexerLoader):
        def _load(self, path):
            return path.split("-")[0], int(path.split("-")[1])

    def assert_eq(seq, cache_size, remain):
        loader = _Loader()
        for s in seq:
            assert s.split("-")[0] == loader.load(s, cache_size=cache_size)
        assert loader.get_cache_items() == remain
        nl = cloudpickle.loads(cloudpickle.dumps(loader))
        assert nl.get_cache_items() == []

    assert_eq(["a-1", "b-2", "c-3", "d-4"], 0, [])
    assert_eq(["a-1", "b-1", "c-1", "d-1"], 2, ["d", "c"])
    assert_eq(["a-1", "b-1", "c-1", "d-1"], 4, ["d", "c", "b", "a"])

    assert_eq(["a-1", "b-1"], 1, ["b"])
    assert_eq(["a-1", "b-2"], 2, ["b"])
    assert_eq(["a-2", "b-1"], 2, ["b"])
    assert_eq(["a-1", "b-3"], 2, ["a"])  # if too large will not check cache

    assert_eq(["a-1", "b-1", "a-1", "a-1"], 2, ["a", "b"])
    assert_eq(["a-1", "b-1", "a-1", "a-1", "c-2"], 2, ["a"])
