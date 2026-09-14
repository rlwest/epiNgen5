"""Pure-Python operations for vector representations."""

import math
from typing import List, Sequence


Vector = Sequence[float]


def _require_same_dimension(left: Vector, right: Vector) -> None:
    if len(left) != len(right):
        raise ValueError(
            f"vectors must have equal dimensions (got {len(left)} and {len(right)})"
        )


def add(left: Vector, right: Vector) -> List[float]:
    """Return the element-wise sum of two equally sized vectors."""
    _require_same_dimension(left, right)
    return [left_value + right_value for left_value, right_value in zip(left, right)]


def scale(vector: Vector, scalar: float) -> List[float]:
    """Return a vector with every element multiplied by ``scalar``."""
    return [scalar * value for value in vector]


def dot(left: Vector, right: Vector) -> float:
    """Return the dot product of two equally sized vectors."""
    _require_same_dimension(left, right)
    return sum(left_value * right_value for left_value, right_value in zip(left, right))


def magnitude(vector: Vector) -> float:
    """Return the Euclidean magnitude of a vector."""
    return math.sqrt(sum(value * value for value in vector))


def normalize(vector: Vector) -> List[float]:
    """Return a unit vector, raising ``ValueError`` for a zero vector."""
    length = magnitude(vector)
    if length == 0:
        raise ValueError("cannot normalize a zero vector")
    return scale(vector, 1.0 / length)


def cosine(left: Vector, right: Vector) -> float:
    """Return cosine similarity, raising ``ValueError`` for a zero vector."""
    _require_same_dimension(left, right)
    denominator = magnitude(left) * magnitude(right)
    if denominator == 0:
        raise ValueError("cosine similarity is undefined for a zero vector")
    return dot(left, right) / denominator


def euclidean(left: Vector, right: Vector) -> float:
    """Return the Euclidean distance between equally sized vectors."""
    _require_same_dimension(left, right)
    return math.sqrt(
        sum(
            (left_value - right_value) ** 2
            for left_value, right_value in zip(left, right)
        )
    )


def convolve(left: Vector, right: Vector) -> List[float]:
    """Return the circular convolution of two equally sized vectors."""
    _require_same_dimension(left, right)
    dimension = len(left)
    return [
        sum(left[index] * right[(output_index - index) % dimension]
            for index in range(dimension))
        for output_index in range(dimension)
    ] if dimension else []


def involution(vector: Vector) -> List[float]:
    """Return the HRR involution: keep the first element and reverse the rest."""
    if not vector:
        return []
    return [vector[0], *reversed(vector[1:])]
