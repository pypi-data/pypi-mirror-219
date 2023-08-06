from pytest import raises
from triad import Schema

from fugue_ml.utils.schema import is_vec_col


def test_is_vec_col():
    schema = Schema("a:int,b:str")
    with raises(KeyError):
        is_vec_col(schema, "c")
    assert not is_vec_col(schema, "a")
    schema = Schema("a:[int],b:[str],c:[float],d:[double]")
    assert is_vec_col(schema, "a")
    assert not is_vec_col(schema, "b")
    assert is_vec_col(schema, "c")
    assert is_vec_col(schema, "d")
