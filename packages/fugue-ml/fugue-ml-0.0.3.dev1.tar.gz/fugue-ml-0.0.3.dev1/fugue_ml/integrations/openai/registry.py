from fugue_ml.embedding import parse_embedding_model, Embedding
from .embedding import OpenAIEmbedding

_DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"


@parse_embedding_model.candidate(
    lambda name, **kwargs: isinstance(name, str)
    and (name == "openai" or name.startswith("openai:"))
)
def _parse_openai_embedding_model(name: str, **kwargs) -> Embedding:
    if name == "openai":
        model_name = _DEFAULT_OPENAI_EMBEDDING_MODEL
    else:
        model_name = name.split(":", 1)[1]
    return OpenAIEmbedding(model_name=model_name, **kwargs)
