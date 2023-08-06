# Vector methods in ALAT (Advanced Linear Algebra Toolkit)

import math
from .matrices import Matrices
from .errors import (
   ZeroLenghtError,
   DimensionError, 
   ZeroVectorError,
   InvertibleMatixError,
   CrossMultiplicationError,
   LinearCombinationError,
)

__all__ = ["Vectors"]

class Vectors:
   """ Vector methods in ALAT.

   Vectors are so important topics in physics and linear algebra.
   So, under 'Vectors' class, I offer basics and advanced vector
   operations.  
   """

   def set_digits(self, value: float, digits: int) -> float:
      """ Set the digits. For example:
      
      >>> result = Vectors().set_digits(-4.10721508, 4)
      >>> print(result)
      -4.107
      """
      sfvalue = str(float(value)) # convert the float to str
      index = 0 # find the index of '.' chars.
      for i in range(len(sfvalue)):
         if sfvalue[i] == '.': break
         index += 1 

      return float(sfvalue[:index + digits + 1])

   def dim(self, vector: tuple) -> int:
      """ Indicate the dimension of `vector`. For example: 
      
      >>> result = Vectors().dim(vector=(4, 7, 0))
      >>> print(result)
      3
      """
      if not isinstance(vector, tuple):
         raise TypeError("'vector' must be tuple")
      
      return len(vector)
   
   def lenght(self, vector: tuple, digits: int = 6) -> float:
      """ Calculate the lenght of `vector`. For example:
       
      >>> result = Vectors().lenght(vector=(5, 12))
      >>> print(result)
      13   
      """
      if not isinstance(vector, tuple):
         raise TypeError("'vector' must be tuple")
      pow = 0 # Sum the each pow of 'vector' points.
      for point in vector:
         pow += point ** 2
      
      return self.set_digits(math.sqrt(pow), digits)
   
   def iszeros(self, vector: tuple) -> bool:
      """ Return True, if `vector` is zeros vector. """
      zeros = []
      # Append the zero  points in the 'zeros' list.
      for point in vector: 
         if point == 0: 
            zeros.append(point)
      if len(zeros) == len(vector): 
         return True
      
      return False
   
   def unit(self, vector: tuple, digits: int = 6):
      """ Calculate the unit vector of `vector`. For example: 
      
      >>> result = Vectors().unit(vector=(3, 4))
      >>> print(result)
      (0.6, 0.8)
      """
      if not isinstance(vector, tuple):
         raise TypeError("'vector' must be tuple")
      # Generate the matrix from 'vector'.
      matrix = [list(vector)]
      # Calculate the lenght of 'vector'.
      lenght = self.lenght(vector, digits)
      # Check if the 'lenght' equals to the zero.
      if lenght == 0:
         raise ZeroLenghtError("'vector' has zero lenght")
      else:
         unit = Matrices().scaler_mul(1/lenght, matrix, digits)

      return tuple(unit[0])

   def add(self, vector1: tuple, vector2: tuple, 
           digits: int = 6) -> tuple: 
      """ Add up the `vector1` and `vector2` vectors. For example:

      >>> vector1 = (3, 4, 5)
      >>> vector2 = (7, -8, -2)
      >>> result = Vectors().add(vector1, vector2)
      >>> print(result)
      (10, -4, 3)
      """
      if not isinstance(vector1, tuple) or \
            not isinstance(vector2, tuple): 
         raise TypeError("'vector1' and 'vector2' must be tuple")
      if len(vector1) != len(vector2):
         raise DimensionError("Found dimension dicrepancy")
      # Add the vectors in here.
      added = []
      for i in range(len(vector1)):
         added.append(vector1[i] + vector2[i])

      return tuple(added)

   def scaler_mul(self, scaler: float, vector: tuple, 
                  digits: int = 6) -> tuple:
      """ Multiply the `scaler` to `vector`. For example: 
      
      >>> vector = (7, -8, -2)
      >>> result = Vectors().scaler_mul(-4, vector)
      >>> print(result)
      (-28.0, 32.0, 8.0)
      """
      if not isinstance(vector, tuple):
         raise TypeError("'vector' must be tuple")
      # Store the multiplied values in here.
      multiplied = []
      for i in range(len(vector)):
         value = vector[i] * scaler
         multiplied.append(self.set_digits(value, digits))
      
      return tuple(multiplied)

   def distance(self, vector1: tuple, vector2: tuple, 
                digits: int = 6) -> float:
      """ Find the distance between `vector1` and `vector2`. For 
      example:

      >>> vector1 = (0, 2, 2)
      >>> vector2 = (2, 0, 1)
      >>> result = Vectors().distance(vector1, vector2)
      >>> print(result)
      3.0
      """
      if not isinstance(vector1, tuple) or \
            not isinstance(vector2, tuple): 
         raise TypeError("'vector1' and 'vector2' must be tuple")
      if len(vector1) != len(vector2):
         raise DimensionError("Found dimension dicrepancy")
      # Append the distances in here.
      distances = 0
      for i in range(len(vector1)):
         distances += (vector1[i] - vector2[i]) ** 2

      return self.set_digits(math.sqrt(distances), digits)

   def dot_mul(self, vector1: tuple, vector2: tuple, 
                digits: int = 6) -> float:
      """ Multiply the `vector1` and `vector2` as dot. For example:

      >>> vector1 = (1, 2, -3)
      >>> vector2 = (3, -2, 4)
      >>> result = Vectors().dot_mul(vector1, vector2)
      >>> print(result)
      -13.0
      """
      if not isinstance(vector1, tuple) or \
            not isinstance(vector2, tuple): 
         raise TypeError("'vector1' and 'vector2' must be tuple")
      if len(vector1) != len(vector2):
         raise DimensionError("Found dimension dicrepancy")
      # Append the multiplied points.
      multiplied = 0
      for i in range(len(vector1)):
         multiplied += vector1[i] * vector2[i]
      
      return self.set_digits(multiplied, digits)

   def iscs(self, vector1: tuple, vector2: tuple) -> bool: 
      """ Return True, if there is Cauchy-Schwarz inequality. """
      if isinstance((vector1, vector2), tuple):
         if len(vector1) == len(vector2):
            eq1 = abs(self.dot_mul(vector1, vector2, 15))
            eq2 = self.dot_mul(vector1, vector1, 15)
            eq3 = self.dot_mul(vector2, vector2, 15)
            if eq2 * eq3 >= eq1:
               return True
      
      return False

   def istri(self, vector1: tuple, vector2: tuple) -> bool: 
      """ Return True, if there is Triangular inequality. """
      if isinstance((vector1, vector2), tuple):
         if len(vector1) == len(vector2):
            eq1 = self.add(vector1, vector2, 15)
            eq1 = self.lenght(eq1, 15)
            eq2 = self.lenght(vector1, 15)
            eq3 = self.lenght(vector2, 15)
            if eq2 + eq3 >= eq1:
               return True
      
      return False

   def ispythag(self, vector1: tuple, vector2: tuple) -> bool: 
      """ Return True, if there is Pythagorean inequality. """
      if isinstance((vector1, vector2), tuple):
         if len(vector1) == len(vector2):
            eq1 = self.add(vector1, vector2, 15)
            eq1 = self.lenght(eq1, 15) ** 2
            eq2 = self.lenght(vector1, 15) ** 2
            eq3 = self.lenght(vector2, 15) ** 2
            if eq2 + eq3 == eq1:
               return True
            
      return False

   def angle(self, method: str, vector1: tuple, vector2: tuple, 
             digits: int = 6) -> float:
      """ Find the angle between `vector1` and `vector2`. `method`
      parameter accept just 'radians', 'decimal' or 'degrees'.
      For example:

      >>> vector1 = (-4, 0, 2, -2)
      >>> vector2 = (2, 0, -1, 1)

      >>> vectors = Vectors()
      >>> print(vectors.angle("decimal", vector1, vector2, 10))
      -1.0
      >>> print(vectors.angle("radians", vector1, vector2, 10))
      3.141592653
      >>> print(vectors.angle("degrees", vector1, vector2, 10))
      180.0
      """
      if not isinstance((vector1, vector2), tuple):
         raise TypeError("'vector1' and 'vector2' must be tuple")
      if len(vector1) != len(vector2):
         raise DimensionError("Found dimension dicrepancy")
      if not method in ("degrees", "radians", "decimal"):
         raise AttributeError("'method' must be 'decimal', "
                              "'radians' or 'degrees'") 
      if self.iszeros(vector1) or self.iszeros(vector2):
         raise ZeroVectorError("Found zeros vector/s")
      # Multiply the 'vector1' and 'vector2' as dot.
      multpilied = self.dot_mul(vector1, vector2, digits)
      pow1, pow2 = 0, 0
      # Get the pow of each the points.
      for point in vector1: pow1 += point ** 2
      for point in vector2: pow2 += point ** 2
      # Calculate the angle in terms of 'decimal'
      angle = multpilied / (math.sqrt(pow1) * math.sqrt(pow2))
      angle = self.set_digits(angle, digits)
      # print(math.acos(-1))
      # Return the 'angle' in proper form according to 'method'.
      if method == "decimal":
         return self.set_digits(angle, digits)
      if method == "radians":
         return self.set_digits(math.acos(angle), digits)
      if method == "degrees":
         degrees = math.degrees(math.acos(angle))
         return self.set_digits(degrees, digits)

   def issteep(self, vector1: tuple, vector2: tuple) -> bool:
      """ Return True, if `vector1` and `vector2` are steeps. """
      if not self.iszeros(vector1) or self.iszeros(vector2):
         if len(vector1) == len(vector2):
            steep = self.angle("degrees", vector1, vector2, 15)
            if steep == 90.0:
               return True
            
      return False

   def isparallel(self, vector1: tuple, vector2: tuple) -> bool:
      """ Return True, if `vector1` and `vector2` are parallels. """
      if not self.iszeros(vector1) or self.iszeros(vector2):
         if len(vector1) == len(vector2):
            steep = self.angle("degrees", vector1, vector2, 15)
            if steep == 180.0:
               return True
            
      return False

   def cross_mul(self, vector1: tuple, vector2: tuple, 
                 digits: int = 6) -> tuple:
      """ Multiply the `vector1` and `vector2` as cross. For example:
      
      >>> vector1 = (1, -2, 1)
      >>> vector2 = (3, 1, -2)
      >>> result = Vectors().cross_mul(vector1, vector2)
      >>> print(result)
      (3.0, 5.0, 7.0)
      """
      if not isinstance((vector1, vector2), tuple):
         raise TypeError("'vector1' and 'vector2' must be tuple")
      if not len(vector1) == len(vector2) == 3:
         raise CrossMultiplicationError("Needs just 3D vectors")
      # Create the 'matrix' and then get the cofactors of it.
      matrix = [[1, 1, 1], list(vector1), list(vector2)]
      cofactors = Matrices().cofactors(matrix, digits)

      return tuple(cofactors[0])

   def lincom(self, vector: tuple, *lincomof: tuple, 
              digits: int = 6) -> tuple:
      """ Write the `vector` as a linear combinations of `lincomof`
      For example: 
      
      >>> vector = (2, 4, 2)
      >>> l1 = (2, 0, 1)
      >>> l2 = (0, 1, 0)
      >>> l3 = (-2, 0, 0)
      >>> result = Vectors().lincom(vector, l1, l2, l3)
      >>> print(result)
      (2.0, 4.0, 1.0)
      # It means:
      (2, 4, 2) = 2.0*(2, 0, 1) + 4.0*(0, 1, 0) + 1.0*(-2, 0, 0)
      """
      # Check if parameters are proper form.
      for v in lincomof:
         if not isinstance((vector, v), tuple):
            raise TypeError("'vector' and 'lincomof' must be tuple")
      # Generate 'matrix' and 'target' and then get the tranposes.
      matrix = Matrices().transpose([list(v) for v in lincomof])
      target = Matrices().transpose([list(vector)])
      # Concatenate the 'matrix' and 'target' and then solve
      # linear equation system.
      concated = Matrices().concat(matrix, target, 1)
      try: # catch a few errors
         solved = Matrices().solve(concated, digits)
      except InvertibleMatixError:
         raise LinearCombinationError(
               "Can not found any linear combination")
      else: # convert the result matrix into vector form
         asvector = Matrices().reshape((1, len(lincomof)), solved)
         return tuple(asvector[0])
   
