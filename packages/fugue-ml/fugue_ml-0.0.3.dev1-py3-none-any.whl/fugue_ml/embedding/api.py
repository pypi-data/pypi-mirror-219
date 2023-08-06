from typing import Any, Optional, Tuple

from fugue import AnyDataFrame

from .base import parse_embedding_model
from .cache import parse_embedding_cache


def compute_embeddings(
    df: AnyDataFrame,
    col: str,
    vec_col: Any,
    model: Any,
    batch_rows: int = 0,
    token_size_range: Optional[Tuple[int, int]] = None,
    on_invalid_token_size: str = "raise",
    cache: Any = None,
    **model_init_kwargs: Any,
) -> AnyDataFrame:
    em = parse_embedding_model(model, **model_init_kwargs)
    return em.encode(
        df,
        col,
        vec_col,
        batch_rows=batch_rows,
        token_size_range=token_size_range,
        on_invalid_token_size=on_invalid_token_size,
        cache=None if cache is None else parse_embedding_cache(cache),
    )


def compute_embedding_input_tokens(
    df: AnyDataFrame,
    col: str,
    model: Any,
    token_size_range: Optional[Tuple[int, int]] = None,
    on_invalid_token_size: str = "raise",
    partition: Any = None,
    summarize: bool = False,
    cache: Any = None,
    **model_init_kwargs: Any,
) -> AnyDataFrame:
    em = parse_embedding_model(model, **model_init_kwargs)
    return em.count_input_tokens(
        df,
        col,
        token_size_range=token_size_range,
        on_invalid_token_size=on_invalid_token_size,
        partition=partition,
        summarize=summarize,
        cache=None if cache is None else parse_embedding_cache(cache),
    )
