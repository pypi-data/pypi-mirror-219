import fugue.api as fa
import pandas as pd
from pytest import raises

from fugue_ml.embedding import FileEmbeddingCache, parse_embedding_model

from .fixtures import MockEmbedding


def test_parse_embedding_model():
    em = parse_embedding_model(MockEmbedding, name="test")
    assert isinstance(em, MockEmbedding)
    assert em.name == "test"
    assert parse_embedding_model(em) is em

    em = parse_embedding_model("_mock", name="test")
    assert isinstance(em, MockEmbedding)
    assert em.name == "test"

    with raises(ValueError):
        parse_embedding_model(1)


def test_embedding(sample_embedding_df, tmpdir):
    # happy path
    em = MockEmbedding("test", mt=3, y=1)
    res = fa.as_array(
        em.encode(sample_embedding_df, "b", "c:[double]", x=1), type_safe=True
    )
    assert res == [
        [1, "a", [1.1, 1.1]],
        [2, "bb", [1.1, 1.1]],
        [2, "ccc", [1.1, 1.1]],
    ]

    # create cache
    cache = FileEmbeddingCache(str(tmpdir.join("cache.parquet")))
    res = fa.as_array(
        em.encode(
            sample_embedding_df.head(2),
            "b",
            "c:[int]",
            cache=cache,
            cache_uid_col="b",
            x=1,
        ),
        type_safe=True,
    )
    assert res == [
        [1, "a", [1, 1]],
        [2, "bb", [1, 1]],
    ]

    # use cache, and update
    res = fa.as_array(
        em.encode(
            sample_embedding_df, "b", "c:[int]", cache=cache, cache_uid_col="b", x=1
        ),
        type_safe=True,
    )
    assert res == [
        [1, "a", [1, 1]],
        [2, "bb", [1, 1]],
        [2, "ccc", [1, 1]],
    ]

    # fully use cache, and update
    res = fa.as_array(
        em.encode(
            sample_embedding_df, "b", "c:[int]", cache=cache, cache_uid_col="b", x=1
        ),
        type_safe=True,
    )
    assert res == [
        [1, "a", [1, 1]],
        [2, "bb", [1, 1]],
        [2, "ccc", [1, 1]],
    ]

    # overwrite token_size_range and skip bad ones
    res = fa.as_array(
        em.encode(
            sample_embedding_df,
            "b",
            "c:[double]",
            batch_rows=1,
            token_size_range=(1, 2),
            on_invalid_token_size="skip",
            x=1,
        ),
        type_safe=True,
    )
    assert res == [
        [1, "a", [1.1, 1.1]],
        [2, "bb", [1.1, 1.1]],
    ]

    # raise on exceeding token_size_range
    em = MockEmbedding("test", mt=2, y=1)
    with raises(ValueError):
        res = fa.as_array(
            em.encode(sample_embedding_df, "b", "c:[int]", x=1), type_safe=True
        )

    # skip on exceeding token_size_range
    res = fa.as_array(
        em.encode(
            sample_embedding_df, "b", "c:[int]", on_invalid_token_size="skip", x=1
        ),
        type_safe=True,
    )
    assert res == [
        [1, "a", [1, 1]],
        [2, "bb", [1, 1]],
    ]
    with raises(ValueError):  # aa doesn't exist
        em.encode(sample_embedding_df, "aa", "c:[double]")

    with raises(ValueError):  # c is not a schema expression
        em.encode(sample_embedding_df, "b", "c")

    with raises(ValueError):  # [str] is not a vector
        em.encode(sample_embedding_df, "b", "c:[str]")

    with raises(ValueError):  # multiple columns
        em.encode(sample_embedding_df, "b", "c:[double],d:[int]")


def test_count_tokens(sample_embedding_df, tmpdir):
    # happy path
    em = MockEmbedding("test", mt=3)
    res = fa.as_array(
        em.count_input_tokens(sample_embedding_df, "b", y=1), type_safe=True
    )
    assert res == [
        [1, "a", 1],
        [2, "bb", 2],
        [2, "ccc", 3],
    ]

    # bad on_invalid_token_size value
    with raises(ValueError):
        fa.as_array(
            em.count_input_tokens(
                sample_embedding_df, "b", on_invalid_token_size="dummy", y=1
            ),
            type_safe=True,
        )

    # overwirte token_size_range, fail on exceeding
    with raises(ValueError):
        fa.as_array(
            em.count_input_tokens(
                sample_embedding_df, "b", token_size_range=(1, 2), y=1
            ),
            type_safe=True,
        )

    # skip on exceeding token_size_range
    res = fa.as_array(
        em.count_input_tokens(
            sample_embedding_df,
            "b",
            token_size_range=(1, 2),
            on_invalid_token_size="skip",
            y=1,
        ),
        type_safe=True,
    )
    assert res == [
        [1, "a", 1],
        [2, "bb", 2],
    ]

    # summarize
    res = list(
        fa.as_dict_iterable(
            em.count_input_tokens(
                sample_embedding_df,
                "b",
                token_size_range=(1, 2),
                on_invalid_token_size="skip",
                summarize=True,
                y=1,
            ),
        )
    )[0]
    assert res == {"b_token_count": 3, "b_row_count": 2}

    # partition and summarize
    res = list(
        fa.as_dict_iterable(
            em.count_input_tokens(
                sample_embedding_df,
                "b",
                token_size_range=(1, 3),
                summarize=True,
                partition="a",
                y=1,
            ),
        )
    )
    assert res == [
        {"a": 1, "b_token_count": 1, "b_row_count": 1},
        {"a": 2, "b_token_count": 5, "b_row_count": 2},
    ]

    # create cache
    cache = FileEmbeddingCache(str(tmpdir.join("cache.parquet")))
    t_em = MockEmbedding("test", mt=3, x=1, y=1)
    res = fa.as_array(
        t_em.encode(
            sample_embedding_df.head(1),
            "b",
            "c:[int]",
            cache=cache,
            cache_uid_col="b",
        ),
        type_safe=True,
    )

    # use cache
    res = list(
        fa.as_dict_iterable(
            em.count_input_tokens(
                sample_embedding_df,
                "b",
                token_size_range=(1, 2),
                on_invalid_token_size="skip",
                summarize=True,
                cache=cache,
                cache_uid_col="b",
                y=1,
            ),
        )
    )[0]
    assert res == {"b_token_count": 2, "b_row_count": 1}

    # all from cache
    res = list(
        fa.as_dict_iterable(
            em.count_input_tokens(
                sample_embedding_df.head(1),
                "b",
                token_size_range=(1, 2),
                on_invalid_token_size="skip",
                summarize=True,
                cache=cache,
                cache_uid_col="b",
                y=1,
            ),
        )
    )[0]
    assert res == {"b_token_count": 0, "b_row_count": 0}
