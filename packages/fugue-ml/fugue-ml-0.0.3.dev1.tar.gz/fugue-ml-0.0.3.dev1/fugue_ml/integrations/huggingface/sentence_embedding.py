from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
import pyarrow as pa
from sentence_transformers import SentenceTransformer

from fugue_ml.embedding import Embedding

from ._utils import GlobalCachedPretrainedTokenizer, HuggingFaceGlobalCachedModel


class GlobalCachedPretrainedSentenceTransformer(
    HuggingFaceGlobalCachedModel[SentenceTransformer]
):
    def __init__(
        self,
        model_name_or_path: Any,
        global_cache_dir: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            id_param="model_name_or_path",
            cache_param="cache_folder",
            global_cache_dir=global_cache_dir,
            model_name_or_path=model_name_or_path,
            **kwargs
        )

    def construct_instance(self, **kwargs: Any) -> SentenceTransformer:
        return SentenceTransformer(**kwargs)


class HuggingFaceSentenceEmbedding(Embedding):
    def __init__(
        self,
        model_name: str,
        model_params: Optional[Dict[str, Any]] = None,
        tokenizing_params: Optional[Dict[str, Any]] = None,
        encoding_params: Optional[Dict[str, Any]] = None,
        global_cache_dir: Optional[str] = None,
    ) -> None:
        super().__init__(
            model_params=model_params,
            tokenizing_params=tokenizing_params,
            encoding_params=encoding_params,
        )
        self.model_name = model_name
        self._tokenizer = GlobalCachedPretrainedTokenizer(
            model_name, global_cache_dir=global_cache_dir, **self.tokenizing_params
        )
        self._model = GlobalCachedPretrainedSentenceTransformer(
            model_name, global_cache_dir=global_cache_dir, **self.model_params
        )

    def token_size_range(self) -> Tuple[int, int]:
        return 1, 512

    def encode_local(
        self,
        df: pd.DataFrame,
        col: str,
        vec_col: str,
        vec_type: pa.DataType,
        **kwargs: Any
    ) -> pd.DataFrame:
        model = self._model.instance
        arr = np.array(
            model.encode(
                df[col].tolist(),
                batch_size=len(df),
                show_progress_bar=False,
                convert_to_numpy=True,
                **kwargs
            ),
            dtype=vec_type.to_pandas_dtype(),
        )
        return df.assign(**{vec_col: list(arr)})

    def count_input_tokens_local(
        self, df: pd.DataFrame, col: str, token_col: str, **kwargs
    ) -> pd.DataFrame:
        enc = self._tokenizer.instance
        return df.assign(**{token_col: df[col].apply(lambda x: len(enc.encode(x)))})
