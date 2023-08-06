import tempfile

import pytest

from fugue_ml.embedding.cache import (
    EmbeddingCache,
    FileEmbeddingCache,
    PandasEmbeddingCache,
    parse_embedding_cache,
)
from fugue_ml.test.embedding.cache_suite import EmbeddingCacheTests


def test_parse_embedding_cache(tmpdir):
    c = parse_embedding_cache("file:" + str(tmpdir.join("x.parquet")))
    assert isinstance(c, FileEmbeddingCache)
    assert parse_embedding_cache(c) is c
    with pytest.raises(ValueError):
        parse_embedding_cache(1)


class PandasEmbeddingCacheTests(EmbeddingCacheTests.Tests):
    def create_cache(self) -> EmbeddingCache:
        return PandasEmbeddingCache()


class FileEmbeddingCacheTests(EmbeddingCacheTests.Tests):
    @pytest.fixture(autouse=True)
    def init_tmpdir(self, tmpdir) -> None:
        self.tmpdir = tmpdir

    def create_cache(self) -> EmbeddingCache:
        tf = self.tmpdir.join("test.parquet")
        return parse_embedding_cache("file:" + str(tf))
