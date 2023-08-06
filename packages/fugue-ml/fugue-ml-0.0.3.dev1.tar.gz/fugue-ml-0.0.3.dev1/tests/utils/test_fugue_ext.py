import fugue.api as fa
import pandas as pd
from pytest import raises

from fugue_ml.utils.fugue_ext import (
    deterministic_shard,
    random_shard,
    replicate,
    deterministic_shard_and_replicate,
)


def test_deterministic_shard():
    df = pd.DataFrame(dict(a=[1, 2, 2], b=[4, 5, 6]))
    res = fa.as_pandas(deterministic_shard(df, 2, "c", ["a"]))
    arr = res.sort_values(["a", "b", "c"]).values.tolist()
    assert arr == [[1, 4, 0], [2, 5, 1], [2, 6, 1]]

    with raises(ValueError):
        deterministic_shard(df, 0, "c", ["a"])

    with raises(ValueError):
        deterministic_shard(df, 2, "c", [])


def test_random_shard():
    df = pd.DataFrame(dict(a=[1, 2, 2], b=[4, 5, 6]))
    res = fa.as_pandas(random_shard(df, 2, "c", seed=0))
    arr = res.sort_values(["a", "b", "c"]).values.tolist()
    assert arr == [[1, 4, 0], [2, 5, 1], [2, 6, 1]]

    res = fa.as_pandas(random_shard(df, 2, "c", seed=1))
    arr = res.sort_values(["a", "b", "c"]).values.tolist()
    assert arr == [[1, 4, 1], [2, 5, 1], [2, 6, 0]]

    with raises(ValueError):
        random_shard(df, 0, "c", ["a"])


def test_replicate():
    df = pd.DataFrame(dict(a=[1, 2], b=[4, 5]))
    res = fa.as_pandas(replicate(df, 2, "c"))
    arr = res.sort_values(["a", "b", "c"]).values.tolist()
    assert arr == [[1, 4, 0], [1, 4, 1], [2, 5, 0], [2, 5, 1]]

    with raises(ValueError):
        replicate(df, 0, "c")


def test_deterministic_shard_and_replicate():
    df = pd.DataFrame(dict(a=[1, 2, 2], b=[4, 5, 6]))
    res = fa.as_pandas(
        deterministic_shard_and_replicate(
            df, 2, "c", ["a"], replicates=2, replicate_col="d"
        )
    )
    arr = res.sort_values(["d", "a", "b", "c", "d"]).values.tolist()
    assert arr == [
        [1, 4, 0, 0],
        [2, 5, 1, 0],
        [2, 6, 1, 0],
        [1, 4, 0, 1],
        [2, 5, 1, 1],
        [2, 6, 1, 1],
    ]

    with raises(ValueError):
        deterministic_shard_and_replicate(
            df, 0, "c", ["a"], replicates=2, replicate_col="d"
        )

    with raises(ValueError):
        deterministic_shard_and_replicate(
            df, 2, "c", [], replicates=2, replicate_col="d"
        )

    with raises(ValueError):
        deterministic_shard_and_replicate(
            df, 2, "c", [], replicates=0, replicate_col="d"
        )
