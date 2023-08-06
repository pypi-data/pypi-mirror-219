from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
import pyarrow as pa
import tiktoken
from openai.embeddings_utils import get_embeddings
from triad import assert_or_throw, run_once

from fugue_ml.embedding import Embedding

from .cred import OpenAICredentialObject


@run_once
def get_encoder(model_name: str) -> tiktoken.Encoding:
    return tiktoken.encoding_for_model(model_name)


class OpenAIEmbedding(Embedding):
    def __init__(
        self,
        model_name: str,
        model_params: Optional[Dict[str, Any]] = None,
        tokenizing_params: Optional[Dict[str, Any]] = None,
        encoding_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            model_params=model_params,
            tokenizing_params=tokenizing_params,
            encoding_params=encoding_params,
        )
        self.model_name = model_name
        self.version = int(model_name.split("-")[-1])
        self.cred = OpenAICredentialObject()

    @property
    def token_size_range(self) -> Tuple[int, int]:
        if self.version <= 1:
            return 1, 2046
        else:
            return 1, 8191

    def encode_local(
        self,
        df: pd.DataFrame,
        col: str,
        vec_col: str,
        vec_type: pa.DataType,
        **kwargs: Any
    ) -> pd.DataFrame:
        assert_or_throw(
            len(kwargs) == 0,
            ValueError("OpenAIEmbedding does not accept extra arguments"),
        )
        arr = np.array(
            get_embeddings(df[col].tolist(), engine=self.model_name),
            dtype=vec_type.to_pandas_dtype(),
        )
        return df.assign(**{vec_col: list(arr)})

    def count_input_tokens_local(
        self, df: pd.DataFrame, col: str, token_col: str, **kwargs: Any
    ) -> pd.DataFrame:
        assert_or_throw(
            len(kwargs) == 0,
            ValueError("OpenAIEmbedding does not accept extra arguments"),
        )
        enc = get_encoder(self.model_name)
        return df.assign(**{token_col: df[col].apply(lambda x: len(enc.encode(x)))})
