from pytest import raises

from fugue_ml.utils.iter import slice_df_by_size_col
import pandas as pd


def test_slice_df_by_size_col():
    def _run(data, **kwargs):
        df = pd.DataFrame(dict(size=data), index=reversed(range(len(data))))
        res = list(slice_df_by_size_col(df, "size", **kwargs))
        return [x["size"].tolist() for x in res]

    assert _run([], size_limit=3) == []
    assert _run([1, 2], size_limit=3) == [[1, 2]]
    assert _run([1, 2, 3], size_limit=3) == [[1, 2], [3]]
    assert _run([1, 2, 3], size_limit=3, row_limit=1) == [[1], [2], [3]]
    with raises(ValueError):
        _run([1, 2, 3], size_limit=2)
    assert _run([1, 2, 3], size_limit=2, ignore_oversize=True) == [[1], [2]]
    assert _run([1, 4, 1], size_limit=3, ignore_oversize=True) == [[1, 1]]
