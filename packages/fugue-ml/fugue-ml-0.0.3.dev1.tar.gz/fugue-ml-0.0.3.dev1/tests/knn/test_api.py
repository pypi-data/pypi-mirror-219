import fugue.api as fa
import numpy as np
import pandas as pd
from pytest import fixture

from fugue_ml.api import compute_knn


@fixture
def index_df():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = arr1 + 0.001
    arr = np.concatenate([arr1, arr2], axis=0)
    return pd.DataFrame(dict(idx=range(len(arr)), dummy=10, vec=list(arr)))


@fixture
def queries():
    arr1 = np.array([[1, 2], [3, 4]])
    arr3 = arr1 - 0.001
    arr = np.concatenate([arr1, arr3], axis=0)
    return pd.DataFrame(dict(q=range(len(arr)), vec=list(arr)))


def test_knn_no_group(index_df, queries):
    res = fa.as_pandas(
        compute_knn(index_df, queries, 2, vec_col="vec", metric="cos", rank_col="rank")
    )

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


def test_knn_with_group(index_df, queries, tmpdir):
    idf = index_df.assign(gg=[0, 0, 1, 1])
    qdf = pd.concat([queries] * 2).assign(gg=[1, 1, 1, 2, 0, 2, 2, 2], q=range(8))

    res = fa.as_pandas(
        compute_knn(
            idf, qdf, 2, vec_col="vec", partition="gg", metric="cos", rank_col="rank"
        )
    )

    expected = {
        (4, 0, 0, 10, 0),
        (4, 0, 1, 10, 1),
        (0, 1, 2, 10, 0),
        (1, 1, 3, 10, 0),
        (2, 1, 2, 10, 0),
        (0, 1, 3, 10, 1),
        (1, 1, 2, 10, 1),
        (2, 1, 3, 10, 1),
    }
    actual = set(
        tuple(x) for x in res[["q", "gg", "idx", "dummy", "rank"]].values.tolist()
    )
    assert actual == expected

    res = fa.as_pandas(
        compute_knn(
            idf,
            qdf,
            2,
            vec_col="vec",
            partition="gg",
            metric="cos",
            rank_col="rank",
            queries_chunk_mem_limit=1,
            broadcast_limit=1,
            temp_path=str(tmpdir),
        )
    )

    actual = set(
        tuple(x) for x in res[["q", "gg", "idx", "dummy", "rank"]].values.tolist()
    )
    assert actual == expected
