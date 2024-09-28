import pytest
from math import isclose, pi
from project.Matrix_Vector_Class import Matrix, Vector


class TestMatrix:
    def test_init(self) -> None:
        matrix = Matrix([[4, 5, 6], [1, 2, 3]])
        assert matrix._Data == [[4, 5, 6], [1, 2, 3]]

        with pytest.raises(TypeError):
            Matrix([[1], [1, 1]])

        with pytest.raises(TypeError):
            Matrix([])

    def test_add_iadd(self) -> None:
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[10, 20], [30, 40]])
        assert (m1 + m2)._Data == [[11, 22], [33, 44]]

        m1 = Matrix([[12, 23], [34, 45]])
        m2 = Matrix([[16, 27], [38, 49]])
        assert (m1 + m2)._Data == [[28, 50], [72, 94]]

        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[1]])
        with pytest.raises(ValueError):
            m1 + m2

        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[1]])
        with pytest.raises(ValueError):
            m1 += m2

    def test_transpose(self) -> None:

        m1 = Matrix([[1, 2], [3, 4], [5, 6]])
        assert m1.T()._Data == [[1, 3, 5], [2, 4, 6]]

        m1 = Matrix([[1]])
        assert m1.T()._Data == [[1]]

    def test_mult(self) -> None:
        # E * A == A is true
        m1 = Matrix([[1, 0], [0, 1]])
        m2 = Matrix([[2, 10], [33, 15]])
        assert (m1*m2)._Data == m2._Data
        
        m1 = Matrix([[1, 0, 0], [0, 1, 0]])
        m2 = Matrix([[2, 10], [33, 15]])
        
        with pytest.raises(ValueError):
            m1 * m2


class TestVector:
    def test_init(self) -> None:
        vec = Vector([[1, 2, 3]])
        assert vec._Data == [[1, 2, 3]]

        vec = Vector([[1], [2], [3]])
        assert vec._Data == [[1], [2], [3]]
        
        with pytest.raises(TypeError):
            Vector([[1,2], [3,4]])
        
        with pytest.raises(TypeError): #vork if vork with matrix
            Vector([[]])
    
    
    def test_dot(self) -> None:
        v1 = Vector([[1], [1], [1]])
        v2 = Vector([[1, 1, 1]])
        assert Vector.dot(v1, v2) == 3
        assert Vector.dot(v2, v1) == 3
        
        v1 = Vector([[1, 2, 3]])
        v2 = Vector([[1, 2]])
        with pytest.raises(ValueError):
            Vector.dot(v1, v2)


    def test_angle(self) -> None:
        v1 = Vector([[0, 0, 0]])
        v2 = Vector([[1, 1, 1]])
        with pytest.raises(ZeroDivisionError):
            Vector.angle(v1, v2)

        v1 = Vector([[1, 0]])
        v2 = Vector([[1, 1, 1]])
        with pytest.raises(ValueError):
            Vector.angle(v1, v2)

        v1 = Vector([[1, 0]])
        v2 = Vector([[1, 1]])
        assert isclose(Vector.angle(v1, v2), pi / 4, abs_tol=1e-5)
    
    
    def test_length(self) -> None:
        # E * A == A is true
        v1 = Vector([[12, 5]])
        assert v1.length() == 13

        v1 = Vector([[0, 0, 0, 0, 0, 0]])
        assert v1.length() == 0

        v1 = Vector([[-1]])
        assert v1.length() == 1
