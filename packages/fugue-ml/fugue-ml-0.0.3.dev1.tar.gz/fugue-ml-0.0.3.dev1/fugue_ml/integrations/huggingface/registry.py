from fugue_ml.embedding import parse_embedding_model, Embedding
from .sentence_embedding import HuggingFaceSentenceEmbedding


@parse_embedding_model.candidate(
    lambda name, **kwargs: isinstance(name, str)
    and name.startswith("sentence-transformers/")
)
def _parse_sentence_transformer_embedding_model(name: str, **kwargs) -> Embedding:
    return HuggingFaceSentenceEmbedding(model_name=name, **kwargs)
