import fugue.api as fa

from fugue_ml.api import compute_embeddings


def test_embedding(sample_embedding_df):
    res = fa.as_array(
        compute_embeddings(
            sample_embedding_df,
            "b",
            "c:[double]",
            "_mock",
            token_size_range=(1, 3),
            name="test",
            mt=2,
            x=1,
            y=1,
        ),
        type_safe=True,
    )
    assert res == [
        [1, "a", [1.1, 1.1]],
        [2, "bb", [1.1, 1.1]],
        [2, "ccc", [1.1, 1.1]],
    ]
    res = fa.as_array(
        compute_embeddings(
            sample_embedding_df,
            "b",
            "c:[int]",
            "_mock",
            token_size_range=(1, 2),
            on_invalid_token_size="skip",
            name="test",
            mt=2,
            x=1,
            y=1,
        ),
        type_safe=True,
    )
    assert res == [
        [1, "a", [1, 1]],
        [2, "bb", [1, 1]],
    ]
