from typing import Any, List, Tuple

import numpy as np
import pandas as pd
import pyarrow as pa
from pytest import fixture

from fugue_ml.embedding import Embedding, parse_embedding_model


@fixture
def sample_embedding_df():
    return pd.DataFrame(dict(a=[1, 2, 2], b=["a", "bb", "ccc"]))


class MockEmbedding(Embedding):
    def __init__(self, name: str, mt: int = 2, x: int = 2, y: int = 2, z: int = 3):
        self.name = name
        self._max = mt
        super().__init__(
            encoding_params=dict(x=x, z=z), tokenizing_params=dict(y=y, z=z)
        )

    @property
    def token_size_range(self) -> Tuple[int, int]:
        return 1, self._max

    def encode_local(
        self,
        df: pd.DataFrame,
        col: str,
        vec_col: str,
        vec_type: pa.DataType,
        **kwargs: Any
    ) -> pd.DataFrame:
        assert kwargs["x"] == 1
        assert kwargs["z"] == 3
        arr = np.ones((len(df), 2)) * 1.1
        arr = arr.astype(vec_type.to_pandas_dtype())
        return df.assign(**{vec_col: list(arr)})

    def count_input_tokens_local(
        self, df: pd.DataFrame, col: str, token_col: str, **kwargs: Any
    ) -> pd.DataFrame:
        assert kwargs["y"] == 1
        assert kwargs["z"] == 3
        return df.assign(**{token_col: df[col].str.len()})


@parse_embedding_model.candidate(
    lambda model, **kwargs: isinstance(model, str) and model == "_mock"
)
def _parse_embedding_model(model: Any, **kwargs: Any) -> Embedding:
    return MockEmbedding(**kwargs)
