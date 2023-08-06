import numpy as np
from typing import Tuple


def compute_dot_product_matrix(vec1: np.array, vec2: np.array) -> np.array:
    """Compute the dot product matrix between the two set of vectors.

    :param vec1: the first set of vectors, shape (n1, d)
    :param vec2: the second set of vectors, shape (n2, d)
    :return: the dot product matrix, shape (n1, n2), where at position (i, j)
        is the dot product between vec1[i] and vec2[j]
    """
    return np.matmul(vec1, vec2.T)


def compute_l2_square_matrix(vec1: np.array, vec2: np.array) -> np.array:
    """Compute the l2 square matrix between the two set of vectors.

    :param vec1: the first set of vectors, shape (n1, d)
    :param vec2: the second set of vectors, shape (n2, d)
    :return: the l2 square matrix, shape (n1, n2), where at position (i, j)
        is the l2 square distance between vec1[i] and vec2[j]
    """
    a2 = np.sum(np.square(vec1), axis=1)
    b2 = np.sum(np.square(vec2), axis=1)
    b2, a2 = np.meshgrid(b2, a2)
    _2ab = compute_dot_product_matrix(vec1, vec2) * 2
    c = a2 + b2 - _2ab
    return c


def compute_cos_sim_matrix(vec1: np.array, vec2: np.array) -> np.array:
    """Compute the cos similarity (1-cos) matrix between the two set of vectors.

    :param vec1: the first set of vectors, shape (n1, d)
    :param vec2: the second set of vectors, shape (n2, d)
    :return: the l2 square matrix, shape (n1, n2), where at position (i, j)
        is 1 - cos(vec1[i], vec2[j])
    """
    norm1 = np.linalg.norm(vec1, 2, axis=1)
    norm2 = np.linalg.norm(vec2, 2, axis=1)
    v1 = vec1 / norm1[:, None]
    v2 = vec2 / norm2[:, None]
    return 1 - compute_dot_product_matrix(v1, v2)


def compute_distance_matrix(vec1: np.array, vec2: np.array, metric: str) -> np.array:
    """Compute the distance matrix between the two set of vectors.

    :param vec1: the first set of vectors, shape (n1, d)
    :param vec2: the second set of vectors, shape (n2, d)
    :param metric: the metric to use, 'l2' or 'cos', 'dot'
    :return: the distance matrix, shape (n1, n2), where at position (i, j)
        is the distance between vec1[i] and vec2[j]

    .. note::

        Smaller distance always means closer:

        * ``l2`` is the square root of the l2 square distance
        * ``cos`` is 1 - cos value of the vectors
        * ``dot`` is the negative value of the dot product.
    """
    if metric == "l2":
        return np.sqrt(compute_l2_square_matrix(vec1, vec2))
    elif metric == "cos":
        return compute_cos_sim_matrix(vec1, vec2)
    elif metric == "dot":
        return -compute_dot_product_matrix(vec1, vec2)
    else:
        raise ValueError(f"Unknown metric {metric}")


def knn(
    index: np.array, queries: np.array, metric: str, k: int
) -> Tuple[np.array, np.array]:
    """The brute force knn search.

    :param index: the set of vectors as index, shape (n1, d)
    :param queries: the set of vectors as queries, shape (n2, d)
    :param metric: the metric to use, 'l2' or 'cos'
    :param k: top k matches with the smallest distance
    :return: the indices and distances of the top k matches for
        each vector in queries, shape (n2, n)
    """
    dist = compute_distance_matrix(queries, index, metric)
    if k == 1:
        idx = np.argmin(dist, axis=1)[:, None]
    elif k < dist.shape[1]:
        idx = np.argpartition(dist, k, axis=1)[:, :k]
    else:
        idx = np.argsort(dist, axis=1)
    res = np.take_along_axis(dist, idx, axis=1)
    return idx, res
