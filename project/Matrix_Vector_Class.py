from math import acos, sqrt
from typing import List
class Matrix:
	"""
	Class wich provide standard operation with matrix
	such as + - * or transpose
	"""
 


	def __init__(self, data: List[List[float]]) -> None:
		"""
		Initializator of matrix.
		Check for correct input
		"""
		
		if (len(data) == 0):
			raise TypeError("width = 0, bad array given")
		
		if (len(data[0]) == 0):
			raise TypeError("first height = 0, bad array given")
		self._Height: int = len(data)
		self._Width: int = len(data[0])
		self._Data = data;
		
		for i in data:
			if (len(i) != self._Width):
				raise TypeError("Data can not be represented as matrix")
	


	def __add__(self, other: "Matrix") -> "Matrix":
		"""
		Return new Matrix wich equal to sum of self and other matrix.
		"""
		if (self._Height != other._Height or self._Width != other._Width):
			raise ValueError("Diferent Dimention of Matrix, Sum cannot be calculated.")
		
		return Matrix(
			
			[
				
				[self._Data[i][j] + other._Data[i][j] for j in range(self._Width)]
			   
				for i in range(self._Height)
				
			]
			
		)
	

	
	def __iadd__(self, other: "Matrix") -> "Matrix":
		"""
		Return Self wich is chenged by adding other matrix.
		"""
		
		if (self._Height != other._Height or self._Width != other._Width):
			raise ValueError("Diferent Dimention of Matrix, Sum cannot be calculated.")
		for i in range(self._Height):
			for j in range(self._Width):
				self._Data[i][j] += other._Data[i][j]
		return self



	def __mul__(self, other: "Matrix") ->"Matrix":
		"""
		Simple matrix multiplier.
		"""
		
		if (self._Width != other._Height):
			raise ValueError("Cannot mult matrises.")
		
		return Matrix(
			[
					 
				[
					sum(
						
						self._Data[i][j] * other._Data[j][k] for j in range(self._Width)
						
					)
					
					for k in range(other._Width)
					
				] 
					  
				for i in range(self._Height)
					
			]
			
		)

	def T(self) -> "Matrix":
		"""
		Simple matrix transpose.
		"""
		return Matrix(list(map(list, zip(*self._Data))))

	def __str__(self) -> str:
		return "\n".join(["\t".join(map(str, row)) for row in self._Data])



class Vector(Matrix):
	"""
	Vecotr - is A matrix with one of dim = 1.
	Add some special operation such as length, dot, angle.
	"""
	def __init__(self, data: List[List[float]]) -> None:
		super().__init__(data)
		
		if (self._Height != 1 and self._Width != 1):
			raise TypeError("Given matrix cannot be represent as vector.")
		
		self._VerticalOrientation: bool = (self._Width == 1)
		
	

	def __len__(self) -> int:
		"""
		Return size of vector.
		"""
		
		if (self._VerticalOrientation):
			return len(self._Data)
		return len(self._Data[0])
	


	def length(self) -> float:
		"""
		Return length of Vector in means of Euclidian spase.
		"""
		
		if (self._VerticalOrientation):
			
			return sqrt(sum([el[0]*el[0] for el in self._Data]))
		
		return sqrt(sum([el*el for el in self._Data[0]]))
	


	@staticmethod
	def dot(first: "Vector", second: "Vector") -> float:
		"""
		Return the simple dot prodoct.
		"""
		
		if (first._VerticalOrientation):
			
			firstM: Matrix = Matrix(first._Data).T()
		
		else:
			
			firstM: Matrix = Matrix(first._Data)
		
		if (not second._VerticalOrientation):
			
			secondM: Matrix = Matrix(second._Data).T()
		
		else:
			
			secondM: Matrix = Matrix(second._Data)
		
		return (firstM * secondM)._Data[0][0]
	


	@staticmethod
	def angle(first: "Vector", second: "Vector") -> float:
		"""
		Return number between 0 and Pi - angle between first and second vectors.
		"""
		
		length1: float = first.length();
		
		length2: float = second.length();
		
		if (length1 == 0 or length2 == 0):
			
			raise ZeroDivisionError(
				
				"Cannot find angle between vectors, where one of them is 0-vector."
				
			)
		
		return acos(Vector.dot(first, second) / (length1 * length2))
	