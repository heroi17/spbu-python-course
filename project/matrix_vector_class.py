from math import acos, sqrt
from typing import List


class Matrix:
    """
    A class for working with matrices.

    Attributes:
        _height "int": A hight of the matrix.
        _width  "int": A width of the matrix.
        _data: "List[List[float]]": A 2D list representing the matrix.

    Methods:
        __init__(self, data: list[list[float]])
            Initializes a Matrix object with the given data.

        __add__(self, other: "Matrix") -> "Matrix"
            Adds two matrices.

        __iadd__(self, other: "Matrix") -> "Matrix"
            Iadds other to self matrix.

        __mul__(other: "Matrix") -> "Matrix"
            Multiplies two matrices.

        T(self) -> "Matrix"
            Returns the transpose of the matrix.

        __str__(self) -> "str"
            Returns a string representation of the matrix.
    """

    def __init__(self, data: List[List[float]]) -> None:
        """
        Initializes a Matrix object.

        Args:
            data "list[list[float]]": A 2D list to create the matrix.
        """

        if len(data) == 0:
            raise TypeError("width = 0, bad array given")
        if len(data[0]) == 0:
            raise TypeError("first height = 0, bad array given")
        self._height: int = len(data)
        self._width: int = len(data[0])
        self._data: List[List[float]] = data
        for i in data:
            if len(i) != self._width:
                raise TypeError("Data can not be represented as matrix")

    def __add__(self, other: "Matrix") -> "Matrix":
        """
        Adds two matrices.

        Args:
            self  "Matrix": The first matrix.
            other "Matrix": The second matrix.

        Returns:
            "Matrix": The resulting matrix after addition.
        """

        if self._height != other._height or self._width != other._width:
            raise ValueError("Diferent Dimention of Matrix, Sum cannot be calculated.")
        return Matrix(
            [
                [self._data[i][j] + other._data[i][j] for j in range(self._width)]
                for i in range(self._height)
            ]
        )

    def __iadd__(self, other: "Matrix") -> "Matrix":
        """
        Iadds second matrix to first matrix.

        Args:
            self  "Matrix": The first matrix.
            other "Matrix": The second matrix.

        Returns:
            "Matrix": The self matrix which changed by iadding other matrix.
        """

        if self._height != other._height or self._width != other._width:
            raise ValueError("Diferent Dimention of Matrix, Sum cannot be calculated.")
        for i in range(self._height):
            for j in range(self._width):
                self._data[i][j] += other._data[i][j]
        return self

    def __mul__(self, other: "Matrix") -> "Matrix":
        """
        Multiply two given matrises.

        Args:
            self  "Matrix": The first matrix.
            other "Matrix": The second matrix.

        Returns:
            "Matrix": The result matrix after multiplication.
        """

        if self._width != other._height:
            raise ValueError("Cannot mult matrises.")
        return Matrix(
            [
                [
                    sum(
                        self._data[i][j] * other._data[j][k] for j in range(self._width)
                    )
                    for k in range(other._width)
                ]
                for i in range(self._height)
            ]
        )

    def T(self) -> "Matrix":
        """
        Find Transpose matrix to given one.

        Args:
            self "Matrix": The matrix to transpose.

        Returns:
            "Matrix": Transposed given matrix.
        """

        return Matrix(list(map(list, zip(*self._data))))

    def __str__(self) -> str:
        return "\n".join(["\t".join(map(str, row)) for row in self._data])


class Vector(Matrix):
    """
    A class for working with vectors.
    Inherits all attributes and Methods from the parent "Matrix" class.

    Attributes:
        _VerticalOrientation ("bool"): A type of oreintation vector (horisont./vertical.)

    Methods:
        __init__(self, data: list[list[float]])
            Initializes a Vector object with the given data.

        length(self) -> float
            Returns the length of the vector in math means.

    Static Methods:
        dot(first: "Vector", second: "Vector") -> float
            Returns the dot product of the vectors.

        angle(first: "Vector", second: "Vector") -> float
            Returns the angle between two vectors in radians.
    """

    def __init__(self, data: List[List[float]]) -> None:
        """
        Initializes a Vector object.

        Parameters:
            data "List[List[float]]": Initial matrix for our vector (should be [1xN] or [Nx1]).
        """

        super().__init__(data)
        if self._height != 1 and self._width != 1:
            raise TypeError("Given matrix cannot be represent as vector.")
        self._VerticalOrientation: bool = self._width == 1

    def length(self) -> float:
        """
        Calculates the length of a vector.

        Args:
            self "Vector": The vector which length we calculate.

        Returns:
            float: The length of the vector.
        """

        if self._VerticalOrientation:
            return sqrt(sum([el[0] * el[0] for el in self._data]))
        return sqrt(sum([el * el for el in self._data[0]]))

    @staticmethod
    def dot(first: "Vector", second: "Vector") -> float:
        """
        Calculates the dot product of two vectors.

        Args:
            first  "Vector": The first vector.
            second "Vector": The second vector.

        Returns:
            float: The dot product of the two vectors.
        """

        firstM: Matrix = Matrix(first._data)
        secondM: Matrix = Matrix(second._data)
        if first._VerticalOrientation:
            firstM = Matrix(first._data).T()
        if not second._VerticalOrientation:
            secondM = Matrix(second._data).T()
        return (firstM * secondM)._data[0][0]

    @staticmethod
    def angle(first: "Vector", second: "Vector") -> float:
        """
        Calculates the angle between two vectors in radians.

        Args:
            first  "Vector": The first vector.
            second "Vector": The second vector.

        Returns:
            float: The angle between the two vectors in radians.
        """

        length1: float = first.length()
        length2: float = second.length()
        if length1 == 0 or length2 == 0:
            raise ZeroDivisionError(
                "Cannot find angle between vectors, where one of them is 0-vector."
            )
        cosVal: float = Vector.dot(first, second) / (length1 * length2)
        # predict problems such as cosVal = +-1.00___02
        if cosVal < -1:
            cosVal = -1
        if cosVal > 1:
            cosVal = 1
        return acos(cosVal)
