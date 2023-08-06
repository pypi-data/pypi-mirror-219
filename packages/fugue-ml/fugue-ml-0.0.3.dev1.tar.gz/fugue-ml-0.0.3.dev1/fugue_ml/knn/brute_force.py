from typing import Any, Tuple

import numpy as np

from fugue_ml.utils.numpy.distance import knn as compute_knn

from .indexer import KNNLocalIndexer, register_knn_indexer


@register_knn_indexer("brute_force")
class BruteForceKNNIndexer(KNNLocalIndexer):
    """Brute force KNN indexer. It is implemented using Numoy and
    It produces exact (perfect) k nearest neighbors.
    """

    def build_local(self, arr: np.ndarray, **kwargs: Any) -> None:
        self._index = arr

    def can_broadcast(self, size_limit: int) -> bool:
        return (
            self._index.nbytes + self._metadata_df.memory_usage(deep=True).sum()
            < size_limit
        )

    def search_local(
        self, queries: np.ndarray, k: int, **kwargs: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        return compute_knn(index=self._index, queries=queries, metric=self.metric, k=k)
