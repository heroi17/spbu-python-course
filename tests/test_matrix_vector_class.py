import pytest
from math import isclose, pi, sqrt
from project.matrix_vector_class import Matrix, Vector
from typing import List


def test_matrix_init() -> None:
    matrix: Matrix = Matrix([[4, 5, 6], [1, 2, 3]])
    assert matrix._data == [[4, 5, 6], [1, 2, 3]]

    with pytest.raises(TypeError):
        Matrix([[1], [1, 1]])

    with pytest.raises(TypeError):
        Matrix([])


@pytest.mark.parametrize(
    "a, b, res",
    [
        (
            [
                [8, 3, 4, -1, -8, -10, -4, 2, -10, 4, -5],
                [-8, -5, 2, -10, 6, 9, 2, 7, 10, 2, 0],
                [-2, 10, 4, 8, -1, -4, 0, 5, 2, -6, -2],
                [10, 8, -7, -7, 4, -5, 1, 10, -2, -7, 5],
                [10, -9, 10, 3, 4, 8, 7, -3, 8, 1, -1],
                [-9, 3, 9, 8, -6, -10, 0, 10, -9, -3, -8],
                [-2, -5, -1, 3, 4, -9, 7, -8, -4, 5, 1],
            ],
            [
                [9, -2, -3, 0, 7, 9, -7, 4, -4, -2, 8],
                [-6, -5, 9, 10, -5, 3, -10, 2, 10, -7, 2],
                [0, -2, -6, 8, -3, -5, -5, -2, 10, 0, 2],
                [-3, 8, -2, -3, -4, 0, 9, -8, -7, -2, 9],
                [-5, -2, -9, -1, 4, -10, -7, 4, -7, -1, -6],
                [-4, 5, -8, 9, 6, -9, -4, -1, 1, 1, 9],
                [7, -4, -2, -10, 8, -5, 8, 10, 6, 1, -9],
            ],
            [
                [17, 1, 1, -1, -1, -1, -11, 6, -14, 2, 3],
                [-14, -10, 11, 0, 1, 12, -8, 9, 20, -5, 2],
                [-2, 8, -2, 16, -4, -9, -5, 3, 12, -6, 0],
                [7, 16, -9, -10, 0, -5, 10, 2, -9, -9, 14],
                [5, -11, 1, 2, 8, -2, 0, 1, 1, 0, -7],
                [-13, 8, 1, 17, 0, -19, -4, 9, -8, -2, 1],
                [5, -9, -3, -7, 12, -14, 15, 2, 2, 6, -8],
            ],
        )
    ],
)
def test_matrix_add_iadd(
    a: List[List[float]], b: List[List[float]], res:  List[List[float]]
) -> None:
    m1: Matrix = Matrix(a)
    m2: Matrix = Matrix(b)
    assert (m1 + m2)._data == res
    m1 += m2
    assert m1._data == res


def test_matrix_add_iadd_correct_input() -> None:
    m1: Matrix = Matrix([[1, 2], [3, 4]])
    m2: Matrix = Matrix([[1]])
    with pytest.raises(ValueError):
        m1 + m2

    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1]])
    with pytest.raises(ValueError):
        m1 += m2


@pytest.mark.parametrize(
    "a, res",
    [
        ([[1, 2, 3, 4, 5, 6]], [[1], [2], [3], [4], [5], [6]]),
        ([[1, 2], [3, 4], [5, 6]], [[1, 3, 5], [2, 4, 6]]),
        ([[1]], [[1]]),
    ],
)
def test_matrix_transpose(a: List[List[float]], res: List[List[float]]) -> None:
    assert Matrix(a).T()._data == res


@pytest.mark.parametrize(
    "a, b, res",
    [
        ([[1, 0], [0, 1]], [[2, 10], [33, 15]], [[2, 10], [33, 15]]),
        (
            [[1, 0], [0, 2], [0, 3]],
            [[1, 3, 8], [2, 6, 9]],
            [[1, 3, 8], [4, 12, 18], [6, 18, 27]],
        ),
    ],
)
def test_matrix_mult(
    a:  List[List[float]], b: List[List[float]], res:  List[List[float]]
) -> None:
    assert (Matrix(a) * Matrix(b))._data == res


def test_matrix_mult_correct_input() -> None:
    m1: Matrix = Matrix([[1, 0, 0], [0, 1, 0]])
    m2: Matrix = Matrix([[2, 10], [33, 15]])
    with pytest.raises(ValueError):
        m1 * m2


def test_vector_init() -> None:
    vec: Vector = Vector([[1, 2, 3]])
    assert vec._data == [[1, 2, 3]]

    vec = Vector([[1], [2], [3]])
    assert vec._data == [[1], [2], [3]]

    with pytest.raises(TypeError):
        Vector([[1, 2], [3, 4]])

    with pytest.raises(TypeError):
        Vector([[]])


@pytest.mark.parametrize(
    "a, b, res",
    [
        ([1, 1, 1], [1, 1, 1], 3),
        ([1, 2, 3], [3, 2, 1], 10),
        ([-1, 2, 3, 1], [2, 4, 5, 0], 21),
    ],
)
def test_vector_dot(a: List[float], b: List[float], res: float) -> None:
    v1: Vector = Vector([[el] for el in a])
    v2: Vector = Vector([b])
    assert Vector.dot(v1, v2) == res


def test_vector_dot_correct_input() -> None:
    v1: Vector = Vector([[1, 2, 3]])
    v2: Vector = Vector([[1, 2]])
    with pytest.raises(ValueError):
        Vector.dot(v1, v2)


@pytest.mark.parametrize(
    "a, b, res",
    [
        ([1, 1, 1], [1, 1, 1], 0),
        ([1, 0, 0], [1, 1, 0], pi / 4),
        ([1, 0, 0, 0], [0, 1, 0, 0], pi / 2),
    ],
)
def test_vector_angle(a: List[float], b: List[float], res: float) -> None:
    assert isclose(Vector.angle(Vector([a]), Vector([b])), res, abs_tol=1e-5)


def test_vector_angle_correct_input() -> None:
    v1: Vector = Vector([[0, 0, 0]])
    v2: Vector = Vector([[1, 1, 1]])
    with pytest.raises(ZeroDivisionError):
        Vector.angle(v1, v2)

    v1 = Vector([[1, 0]])
    v2 = Vector([[1, 1, 1]])
    with pytest.raises(ValueError):
        Vector.angle(v1, v2)


@pytest.mark.parametrize(
    "a, res",
    [
        ([1, 0, 0], 1),
        ([4, 3, 0, 0], 5),
        ([1, 1, 0], sqrt(2)),
        ([1.1, 2.2], 1.1 * sqrt(5)),
        ([0, 0, 0, 0], 0),
        ([-12, 0, 5], 13),
        ([-1], 1),
    ],
)
def test_vector_length(a: List[float], res: float) -> None:
    assert isclose((Vector([a])).length(), res, abs_tol=1e-4)
