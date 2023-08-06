# Matrix methods in ALAT (Advanced Linear Algebra Toolkit)

import math
import random as _random
from .errors import (
   MatrixError, 
   SquareMatrixError,
   ModeError,
   DimensionError,
   MinorsError, 
   CofactorsError, 
   InvertibleMatixError,
)

__all__ = ["Matrices"]

class Matrices:
   """ Matrix methods in ALAT 
   
   This class offers so many matrix methods. Matrices are so hot 
   topic in linear algerba. Especially, in engineering or scientific
   researhes, it is used for most time. So, under 'Matrices' class
   I offer so many basics and advanced matrix operations.
   """

   # ----------------------------------------------------------------
   # ----------------------- Basics Methods -------------------------
   # ----------------------------------------------------------------

   def set_digits(self, value: float, digits: int) -> float:
      """ Set the digits. For example:
      
      >>> result = Matrices().set_digits(-4.10721508, 4)
      >>> print(result)
      -4.107
      """
      sfvalue = str(float(value)) # convert the float to str
      index = 0 # find the index of '.' chars.
      for i in range(len(sfvalue)):
         if sfvalue[i] == '.': break
         index += 1 

      return float(sfvalue[:index + digits + 1])

   def ismatrix(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` has consistent defination. """
      # Itself and rows of 'matrix' must be list form. 
      if not isinstance(matrix, list): return False
      for row in matrix: 
         if not isinstance(row, list): return False
         # Also, 'matrix' must have same row or column numbers.
         if len(row) != len(matrix[0]): return False 
      return True
   
   def dim(self, matrix: list[list]) -> tuple:
      """ Return the dimension of `matrix`. For example:
       
      >>> matrix = [
         [4, 7, 3], 
         [0, 1, 9], 
      ]  
      >>> result = Matrices().dim(matrix)
      >>> print(result)
      (2, 3)
      """
      if not self.ismatrix(matrix): 
         raise MatrixError("Inconsistent matrix defination")
      return (len(matrix), len(matrix[0])) # (row, col)
   
   def issquare(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` is square. """
      if self.ismatrix(matrix) and len(matrix) == len(matrix[0]):
         return True
      return False
   
   def diagonal(self, matrix: list[list]) -> list[list]:
      """ Extract the main diagonal of `matrix`. For example:
       
      >>> matrix = [
         [4, 3, 0], 
         [1, 5, 7], 
         [0, 3, 8],
      ] 
      >>> result = Matrices().diagonal(matrix)
      >>> print(result)
      [[4.0, 5.0,  8.0]]
      """
      if not self.issquare(matrix): 
         raise SquareMatrixError("'matrix' must be square")
      # Put the main diagonal of 'matrix' in another matrix.
      return [[float(matrix[i][i]) for i in range(len(matrix))]]
   
   def ishomogen(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` is homogen. """
      if self.ismatrix(matrix):
         # Homogeneous matrix contains zero in last of each row.
         homo = [1 for i in range(len(matrix)) if matrix[i][-1]==0]
         if len(homo) == len(matrix): 
            return True
      return False
   
   def iszeros(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` just contains zeros. """
      if self.ismatrix(matrix):
         # Collect the all elements of 'matrix'.
         alls = [value for row in matrix for value in row]
         # Select the just zeros in the 'alls'.
         zeros = [0 for value in alls if value == 0]
         if len(alls) == len(zeros): return True
      return False
   
   def isones(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` just contains ones. """
      if self.ismatrix(matrix):
         # Collect the all elements of 'matrix'.
         alls = [value for row in matrix for value in row]
         # Select the just ones in the 'alls'.
         ones = [0 for value in alls if value == 1]
         if len(alls) == len(ones): return True
      return False

   def isidentity(self, matrix: list[list]) -> bool: 
      """ Return True, if `matrix` is identity matrix. """
      if self.issquare(matrix):
         # Collect the all elements of 'matrix'.
         alls = [value for row in matrix for value in row]
         # Select the just zeros in the 'alls'.
         zeros = [0 for value in alls if value == 0]
         # Select the just ones in the 'alls'.
         ones = [1 for value in alls if value == 1]
         if len(alls) == len(ones) + len(zeros) and \
            [ones] == self.diagonal(matrix): return True
      return False

   def zeros(self, dim: tuple) -> list[list]:
      """ Generate the zeros matrix. For example: 
      
      >>> result = Matrices().zeros(dim=(3, 3))
      >>> print(result)
      [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
      """
      if not isinstance(dim, tuple):
         raise TypeError("'dim' must be tuple")
      if len(dim) != 2:
         raise AttributeError( 
            "'dim' must just contain row and column info"
         )
      row = [float(0) for x in range(dim[1])]  
      matrix = [list(row) for x in range(dim[0])] 
      return matrix

   def ones(self, dim: tuple) -> list[list]: 
      """ Generate the ones matrix. For example: 
      
      >>> result = Matrices().ones(dim=(3, 3))
      >>> print(result)
      [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
      """
      if not isinstance(dim, tuple):
         raise TypeError("'dim' must be tuple")
      if len(dim) != 2:
         raise AttributeError(
            "'dim' must contain just row and column info"
         )
      row = [float(1) for x in range(dim[1])]  
      matrix = [list(row) for x in range(dim[0])] 
      return matrix

   def identity(self, dim: tuple) -> list[list]: 
      """ Generate the identity matrix. For example: 
      
      >>> result = Matrices().identity(dim=(3, 3))
      >>> print(result)
      [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
      """
      # Derivate the identity matrix from zeros matrix.
      matrix = self.zeros(dim=dim)
      # Check if 'matrix' is square or not.
      if not self.issquare(matrix):
         raise SquareMatrixError(
            'Matrix which will be generated must be square'
         )
      # Replace the main diagonal of 'matrix' with ones. 
      for i in range(len(matrix)): matrix[i][i] = 1.0
      return matrix

   def arbitrary(self, value: float, dim: tuple) -> list[list]: 
      """ Generate the arbitrary matrix which just contain `value`. 
      For example: 
      
      >>> result = Matrices().arbitrary(value=4, dim=(3, 3))
      >>> print(result)
      [[4.0, 4.0, 4.0], [4.0, 4.0, 4.0], [4.0, 4.0, 4.0]]
      """
      if not isinstance(value, (int, float)):
         raise TypeError("'value' must be int or float")
      if not isinstance(dim, tuple): 
         raise TypeError("'dim' must be tuple")
      if len(dim) != 2:
         raise ValueError( 
            "'dim' must just contain row and column info"
         )
      row = [float(value) for x in range(dim[1])] 
      matrix = [list(row) for x in range(dim[0])] 
      return matrix

   def sequential(self, interval: tuple, dim: tuple, 
                  digits: int = 6) -> list[list]:
      """ Generate the sequential matrix. For example:

      >>> matrices = Matrices().sequential(interval=(1, 100), 
                                           dim=(4, 5))
      >>> print(result)
      [[1.0, 6.21052, 11.421, 16.6315, 21.8421], [27.0526, 32.2631, 
      37.4736, 42.6842, 47.8947], [53.1052, 58.3157, 63.5263, 68.
      7368, 73.9473], [79.1578, 84.3684, 89.5789, 94.7894, 100.0]]
      """
      if not isinstance(interval, tuple) or \
         not isinstance(dim, tuple):
         raise TypeError( "'interval' and 'dim' must be tuple")
      if len(interval) != 2 or len(dim) != 2:
         raise ValueError(
            "'interval' and 'dim' must just contain two values"
         )
      # Indicate the step interval.
      step = (interval[1] - interval[0]) / (dim[0] * dim[1] -1)
      # Find the elements that will be added into matrix.
      total = interval[0] 
      # Can be used any matrix. Already, all elements are changed.
      matrix = self.zeros(dim=dim)
      # Fill in the 'matrix' with the new elements.
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            matrix[i][j] = self.set_digits(total, digits)
            total += step # in each iteration, update the 'total'

      return matrix 

   def random(self, dim: tuple, digits: int=6) -> list[list]: 
      """ Generate the random matrix which just contains numbers
      between 0 and 1. For example: 

      >>> result = Matrices().random(dim=(5, 6))
      >>> print(result)
      [[0.50165, 0.91821, 0.21523, 0.17739, 0.90766, 0.06914], [0.
      24665, 0.63955, 0.47908, 0.8836, 0.93313, 0.07537], [0.86464, 
      0.57829, 0.1691, 0.15268, 0.48396, 0.39225], [0.90855, 0.
      99932, 0.77091, 0.20381, 0.15557, 0.10508], [0.39042, 0.53123, 
      0.82926, 0.76104, 0.86319, 0.70947]]
      """
      if not isinstance(dim, tuple):
         raise TypeError("'dim' must be tuple")
      if len(dim) != 2:
         raise ValueError(
            "'dim' must just contain row and column info"
         )
      # Generate the zeros matrix and replace the elements.
      matrix = self.zeros(dim=dim)
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            # Generate the random number
            random = self.set_digits(_random.random(), digits)
            matrix[i][j] = random

      return matrix

   def uniform(self, interval: tuple, dim: tuple, 
               digits: int = 6) -> list[list]:
      """ Generate the uniform matrix. For example:

      >>> result = Matrices().uniform(interval=(1, 100), dim=(3, 5))
      >>> print(result) 
      [[16.2854, 12.8651, 63.5494, 55.2237, 95.523], [78.4118, 
      98.0577, 59.7269, 64.9273, 86.5067], [12.7045, 53.0264, 
      99.8104, 10.5167, 37.1275]]
      """
      if not isinstance(interval, tuple) or \
         not isinstance(dim, tuple):
         raise TypeError("'interval' and 'dim' must be tuple")
      if len(interval) != 2 or len(dim) != 2:
         raise ValueError(
            "'interval' and 'dim' must just contain two values"
         )
      # Generate the zeros matrix and then replace the elements.
      matrix = self.zeros(dim=dim)
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            # Generate the uniform number
            matrix[i][j] = self.set_digits(
               _random.uniform(interval[0], interval[1]), digits
            )
      return matrix
   
   def randint(self, interval: tuple, dim: tuple) -> list[list]: 
      """ Generate the randint matrix. For example:

      >>> result = Matrices().randint(interval=(10, 50), dim=(4, 5))
      >>> print(result) 
      [[17, 23, 27, 55, 18], [39, 84, 96, 60, 99], [95, 23, 61, 33, 
      28], [75, 53, 93, 21, 62]]
      """
      if not isinstance(interval, tuple) or \
         not isinstance(dim, tuple):
         raise TypeError("'interval' and 'dim' must be tuple")
      if len(interval) != 2 or len(dim) != 2:
         raise ValueError(
            "'interval' and 'dim' must just contain two values"
         )
      # Generate the zeros matrix and then replace the elements.
      matrix = self.zeros(dim=dim)
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            # Generate the uniform number.
            matrix[i][j] = _random.randint(interval[0], interval[1])

      return matrix
   
   def highest(self, matrix: list[list]) -> float:
      """ Return the highest value in `matrix`. For example: 
      
      >>> matrix = [
         [4, 7, 3], 
         [0, 7, 9], 
         [3, 6, 7], 
      ]
      >>> result = Matrices().highest(matrix)
      >>> print(result)
      9.0
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Select the highest element of 'matrix'.
      return float(max([el for row in matrix for el in row])) 


   def lowest(self, matrix: list[list]) -> float: 
      """ Return the lowest value in `matrix`. For example: 
      
      >>> matrix = [
         [4, 7, 3], 
         [0, 7, 9], 
         [3, 6, 7], 
      ]
      >>> result = Matrices().lowest(matrix)
      >>> print(result)
      0.0
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Select the lowest element of 'matrix'.
      return float(min([el for row in matrix for el in row])) 

   def aggregate(self, matrix: list[list], 
                 axis: int = 0) -> list[list]: 
      """ Aggreagate the `matrix` according to `axis`. `axis` must
      be 0 (horizontal) or 1 (vectical). For example:
   
      >>> matrix = [
         [4, 7, 1], 
         [3, 1, 5], 
         [0, 8, 9], 
      ]
      
      ## Example 1:
      >>> result = Matrices().aggregate(matrix, axis=0)
      >>> print(result)
      [[7.0, 16.0, 15.0]]
      
      ## Example 2:
      >>> result = Matrices().aggregate(matrix, axis=1)
      >>> print(result)
      [[12.0], [9.0], [17.0]]
      """
      total = 0
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      if not axis in (0, 1):
         raise ValueError("'axis' must be 0 or 1")
      # 0 (zero) represents horizontal axis.
      if axis == 0:
         # Generate the zeros matrix and replace the elements.
         aggregated = self.zeros(dim=(1, len(matrix[0])))
         for i in range(len(matrix[0])):
            for row in matrix:
               total += row[i]
            # Save the aggregated elements into 'matrix'.
            aggregated[0][i] = float(total)
            total = 0
      # 1 (one) reoresents vertical axis.
      if axis == 1:
         # Generate the zeros matrix and replace the elements.
         aggregated = self.zeros(dim=(len(matrix), 1))
         for i in range(len(matrix)):
            for j in range(len(matrix[0])):
               total += matrix[i][j]
            # Save the aggregated elements into 'matrix'.
            aggregated[i][0] = float(total)
            total = 0

      return aggregated

   def iselementary(self, matrix: list[list]) -> bool:
      """ Return True, if `matrix` is elementary. """
      diffirent = []
      if self.issquare(matrix):
         # Declare the identity matrix for initialize matrix.
         identity = self.identity(dim = self.dim(matrix))
         # Iterate the 'matrix'.
         for i in range(len(matrix)):
            for j in range(len(matrix[0])):
               if not matrix[i][j] == identity[i][j]:
                  diffirent.append(matrix[i][j])
         # If 'identity' matrix was changed by one any operation
         # and then was created 'matrix'.
         if len(diffirent) == 1 and diffirent[0] != 0:
            return True
         # If the rows of 'matrix' was changed with each other.
         if self.ones(dim = (1, len(matrix))) == \
            self.aggregate(matrix, 0):
            return True
      
      return False

   def mean(self, matrix: list[list], digits: int=6) -> float:
      """Calculate mean of `matrix`. For example:
   
      >>> matrix = [
         [4, -2, 0], 
         [7, 6, -1],
         [-9, 0, 4], 
      ]
      >>> result = Matrices().mean(matrix)
      >>> print(result)
      1.0   
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Sum the all elements and then divide it to total elements.
      s = sum([el for row in matrix for el in row])
      m = s / (len(matrix) * len(matrix[0]))

      return self.set_digits(value=m, digits=digits)
   
   def sort(self, matrix: list[list], 
            reverse: bool = False) -> list[list]:
      """ Sort the `matrix` elements according to `reverse` 
      parameter. For example: 
      
      >>> matrix = [
         [8, -2, 4], 
         [0, -5, 0]
      ]
      ## Example 1
      >>> result = Matrices().sort(matrix)
      >>> print(result)
      [[-5, -2, 0], [0, 4, 8]]

      ## Example 2
      >>> result = Matrices().sort(matrix, reverse=True)
      >>> print(result)
      [[8, 4, 0], [0, -2, -5]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Previously, gather the all element in a list.
      elements = [matrix[i][j] for i in range(len(matrix)) 
                               for j in range(len(matrix[0]))]
      # Sort the elements.
      elements.sort(reverse=reverse)
      # And then, again convert the 'elements' to matrix.
      index  = 0 # index of 'elements' list.
      # Initilialy, generate the zeros matrix
      ordered = self.zeros(dim=self.dim(matrix))
      # and then fill in it with 'elements'. 
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            ordered[i][j] = elements[index]
            index += 1
      
      return ordered
   
   def stdev(self, matrix: list[list], digits: int = 6) -> float:
      """ Calculate the standard deviation of `matrix`. For example:
      
      >>> matrix = [[85, 86, 100, 76, 81, 93, 84, 99, 71, 69, 93, 
                     85, 81, 87, 89]]
      >>> result = Matrices().stdev(matrix)
      >>> print(result)
      8.698
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Calculate the mean of 'matrix'.
      mean = self.mean(matrix, digits) 
      total_pow = 0
      # Iterate the 'matrix' elements.
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            # Subtract each elements from mean and add it to 'pow'.
            total_pow += math.pow(abs(mean - matrix[i][j]), 2)
      # Divide the 'total_pow' to number of the 'matrix' element.
      stdev = math.sqrt(total_pow/(len(matrix) * len(matrix[0])))

      return self.set_digits(stdev, digits)
   
   def mode(self, matrix: list[list]) -> list[list]: 
      """ Return the mode or modes of `matrix`. If there is not any
      mode/s, raise error. For example:

      ## Example 1
      >>> matrix = [
         [4, 7, 0, -2], 
         [-2, -5, 7, 3],
      ]
      >>> result = Matrices().mode(matrix)
      >>> print(result)
      [[-2, 7]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Mode means the value/s that repeats mostly.
      els = [el for row in matrix for el in row]
      # If there is not any mode/s return error.
      if len(els) == len(list(set(els))):
         raise ModeError("Can not found any mode/s")
      # Find how many times which elements is repeated. 
      repreated = {value: els.count(value) for value in els} 
      # Find mostly repeated the elements of 'matrix'
      modes = []
      # and put these elements into 'modes' matrix.
      for key, value in repreated.items():
         if repreated[key] == max(repreated.values()):
            modes.append(key)

      return [modes]

   def median(self, matrix: list[list]) -> float: 
      """ Return the median of 'matrix'. For example:

      >>> matrix = [
         [7, 2, 6], 
         [-3, -5, 0]
      ]
      >>> result = Matrices().median(matrix)
      >>> print(result)
      1.0
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Pool the all elements into an array.
      median = [el for row in matrix for el in row]
      # Sort the elements in ascending order.
      median.sort()
      # Calculate the median.
      if len(median) % 2 == 1:
         return float(median[round(len(median)/2)-1])
      else:
         first, second = int(len(median)/2-1), int(len(median)/2)
         return (median[first] + median[second]) / 2

   def shuffle(self, matrix: list[list]) -> list[list]: 
      """ Shuffle the `matrix`. For example: 
      >>> matrix = [
         [6, 4, 0], 
         [-2, -2, 7], 
         [0, -1, 0]
      ]
      >>> result = Matrices().shuffle(matrix)
      >>> print(result)
      [[-2, 0, -1], [-2, 7, 0], [6, 0, 4]]

      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Gather all the elements into an array.
      shuffle = [matrix[i][j] for i in range(len(matrix)) 
                              for j in range(len(matrix[0]))]
      # Shuffle the 'shuffle'.
      _random.shuffle(shuffle)
      index = 0
      # Lastly, generate the shuffled matrix over zeros matrix.
      shuffled = self.zeros(dim=self.dim(matrix))
      for i in range(len(matrix)):
         for j in range(len(matrix)):
            shuffled[i][j] = shuffle[index]
            index += 1

      return shuffled
   
   def reshape(self, dim: tuple, matrix: list[list]) -> list[list]:
      """ Reshape the `matrix` with `dim` parameter. For example: 
      >>> matrix = [
         [6, 4, 0], 
         [-2, -2, 7], 
         [0, -1, 0]
      ]
      >>> result = Matrices().reshape((1, 9), matrix)
      >>> print(result)
      [[6, 4, 0, -2, -2, 7, 0, -1, 0]]

      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      if not isinstance(dim, tuple):
         raise TypeError("'dim' must be tuple")
      if len(dim) != 2:
         raise ValueError(
            "'dim' must just contain row and column info"
         )
      if not len(matrix) * len(matrix[0]) == dim[0] * dim[1]:
         raise DimensionError("Found dimension dicrepancy")
      # Transmit the elements of 'matrix' into 'els'.
      index = 0
      els = [matrix[i][j] for i in range(len(matrix))
                          for j in range(len(matrix[0]))]
      # Generate the zeros matrix 
      zeros = self.zeros(dim=dim)
      # and then replace the its elements with 'els' elements.
      for i in range(dim[0]):
         for j in range(dim[1]):
            zeros[i][j] = els[index]
            index += 1

      return zeros

   def transpose(self, matrix: list[list]) -> list[list]: 
      """ Get the transpose of `matrix`. For example: 
      >>> matrix = [
         [6, 4, 0], 
         [-2, -2, 7], 
      ]
      >>> result = Matrices().transpose(matrix)
      >>> print(result)
      [[6, -2], [4, -2], [0, 7]]

      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Change the row and columns with each other.
      trans = self.zeros(dim=(len(matrix[0]), len(matrix)))
      for j in range(len(matrix[0])):
         for i in range(len(matrix)):
            trans[j][i] = matrix[i][j]

      return trans

   def concat(self, matrix1: list[list], matrix2: list[list], 
              axis: int = 0): 
      """ Concatenates `matrix1` and `matrix2` according to `axis`.
      For example: 

      >>> matrix1 = [
         [6, 4], 
         [-2, -2]
      ]
      >>> matrix2 = [
         [7, 8], 
         [0, 0],
      ]
      >>> result = Matrices().concat(matrix1, matrix2, axis=0)
      >>> print(result)
      [[6, 4], [-2, -2], [7, 8], [0, 0]]

      >>> result = Matrices().concat(matrix1, matrix2, axis=1)
      >>> print(result)
      [[6, 4, 7, 8], [-2, -2, 0, 0]]
      """
      if not self.ismatrix(matrix1) or not self.ismatrix(matrix2):
         raise MatrixError("Inconsistent matrix defination")
      if not axis in (0, 1):
         raise AttributeError("'axis' must be 0 or 1")
      if (axis == 0 and len(matrix1[0]) != len(matrix2[0])) or \
         axis == 1 and len(matrix1) != len(matrix2):
         raise DimensionError("Found dimension dicrepancy")
      # Copy the 'matrix1' for new matrix.
      matrix = matrix1.copy()
      # axis 0 means, concatenates the two matrices as horizontal.
      if axis == 0:
         for row in matrix2:
            matrix.append(row)
      # axis 1 means, concatenates the two matrices as vertical.
      if axis == 1:
         for i in range(len(matrix)):
            matrix[i] = matrix[i] + matrix2[i]
      
      return matrix
      
   def islowertri(self, matrix: list[list]) -> bool: 
      """ Return True, if `matrix` is lower triangular. """
      islower = []
      if self.issquare(matrix): # 'matrix' must be square
         for i in range(len(matrix)-1):
            for el in matrix[i][i+1:]:
               islower.append(el)
         if [islower] == self.zeros(dim=(1, len(islower))):
            return True
      return False
   
   def isuppertri(self, matrix: list[list]) -> bool: 
      """ Return True, if `matrix` is upper triangular. """
      if self.issquare(matrix): # 'matrix' must be square
         # Get the transpose 'matrix' and then
         transposed = self.transpose(matrix)
         # check if it is lower triangular matrix.
         if self.isltri(transposed):
            return True
      return False

   def istriangle(self, matrix: list[list]) -> bool: 
      """ Return true, if `matrix` is lower or upper triangular. """
      if self.isltri(matrix) or self.isltri(matrix):
         return True
      return False

   def add(self, matrix1: list[list], matrix2: list[list], 
           digits: int = 6) -> list[list]: 
      """ Add up the `matrix1` and `matrix2` with each other. 
      For example:

      >>> matrix1 = [
         [6, 1, 7], 
         [1, -2, 0]
      ]
      >>> matrix2 = [
         [7, 8, 6], 
         [0, 0, -1],
      ]
      >>> result = Matrices().add(matrix1, matrix2, digits=6)
      >>> print(result)
      [[13.0, 9.0, 0.0], [1.0, -2.0, 0.0]]
      """
      if not (self.ismatrix(matrix1) or self.ismatrix(matrix2)):
         raise MatrixError("Inconsistent matrix defination")
      if not self.dim(matrix1) == self.dim(matrix2):
         raise DimensionError("Found dimension dicrepancy")
      # Initialy, generate the zeros matrix 
      matrix = self.zeros(dim=self.dim(matrix1))
      # and then add up the matrices.
      for i in range(len(matrix1)):
         for j in range(len(matrix2[0])):
            total = matrix1[i][j] + matrix2[i][j]
            matrix[i][j] = self.set_digits(total, digits)

      return matrix

   def scaler_mul(self, scaler: float, matrix: list[list], 
                  digits: int = 6) -> list[list]: 
      """ Multiply the `scaler` and `matrix` with each other. 
      For example:

      >>> matrix = [
      [7, 8, 6], 
      [0, 0, -1],
      ]
      >>> result = Matrices().scaler_mul(4.12345, matrix2, digits=6)
      >>> print(result)
      [[28.8641, 32.9876, 24.7407], [0.0, 0.0, -4.12345]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Copy the 'matrix' elements
      multiplied = matrix.copy()
      # and then multiply those with 'scaler'.
      for i in range(len(multiplied)):
         for j in range(len(multiplied[0])):
            mul = scaler * multiplied[i][j]
            multiplied[i][j] = self.set_digits(mul, digits)

      return multiplied

   def subtract(self, matrix1: list[list], matrix2: list[list], 
                digits: int = 6) -> list[list]:
      """ Subtract the `matrix2` from  `matrix1`. For example:
                
      >>> matrix1 = [
         [6, 1, 7], 
         [1, -2, 0],
      ]
      >>> matrix2 = [
         [7, 8, 6], 
         [0, 0, -1],
      ]
      >>> result = Matrices().subtract(matrix1, matrix2)
      >>> print(result)
      [[-1.0, -7.0, 1.0], [1.0, -2.0, 1.0]]
      """
      if not (self.ismatrix(matrix1) or self.ismatrix[matrix2]):
         raise MatrixError("Inconsistent matrix defination")
      if not self.dim(matrix1) == self.dim(matrix2):
         raise DimensionError("Found dimension dicrepancy")
      # Shortly, can be used 'scaler_mul' and 'add' methods.
      multiplied = self.scaler_mul(-1, matrix2, digits)
      return self.add(matrix1, multiplied, digits)
   
   def dot_mul(self, matrix1: list[list], matrix2: list[list], 
               digits: int = 6) -> list[list]: 
      """ Multiply the `matrix1` and `matrix2` with each other 
      as dot. For example:

      >>> matrix1 = [
         [6, 1, 7], 
         [1, -2, 0],
      ]
      >>> matrix2 = [
         [7, 8, 6], 
         [0, 0, -1],
      ]
      >>> result = Matrices()
      >>> print(result.dot_mul(matrix1, matrix2))
      [[42, 8, 42], [0, 0, 0]]
      """
      if not (self.ismatrix(matrix1) or self.ismatrix(matrix2)):
         raise MatrixError("Inconsistent matrix defination")
      if not self.dim(matrix1) == self.dim(matrix2):
         raise DimensionError("Found dimension dicrepancy")
      # Initially, generate the zeros matrix
      zeros = self.zeros(dim=self.dim(matrix1))
      # and then fill the elements in it.
      for i in range(len(matrix1)):
         for j in range(len(matrix1[0])):
            zeros[i][j] = matrix1[i][j] * matrix2[i][j]

      return zeros

   def cross_mul(self, matrix1: list[list], matrix2: list[list], 
                 digits: int = 6) -> list[list]: 
      """ Multiply the `matrix1` and `matrix2` with each other 
      as cross. For example: 
       
      >>> matrix1 = [
         [1, -2, 4, 0], 
         [3, 0, -2, -2],
      ]
      >>> matrix2 = [
         [4, -7], 
         [-3, 0], 
         [-1, 1],
         [-5, -4],
      ]
      >>> result = Matrices().cross_mul(matrix1, matrix2)
      >>> print(result)
      [[6, -3], [24, -15]]
      """
      if not (self.ismatrix(matrix1) or self.ismatrix(matrix2)):
         raise MatrixError("Inconsistent matrix defination")
      if len(matrix1[0]) != len(matrix2):
         raise DimensionError("Found dimension dicrepancy")
      # Initially, generate the zeros matrix and then 
      # fill the elements in here.
      matrix = self.zeros(dim=(len(matrix1), len(matrix2[0])))
      total = 0
      # Get the transpose of 'matrix2'.
      matrix2 = self.transpose(matrix2)
      # Lastly, multiply the elements.
      for i in range(len(matrix1)):
         for j in range(len(matrix2)):
            for k in range(len(matrix2[0])):
               total += matrix1[i][k] * matrix2[j][k]
            matrix[i][j] = self.set_digits(total, digits)
            total = 0

      return matrix

   def scaler_div(self, scaler: float, matrix: list[list], 
                  digits: int = 6): 
      """ Divide the `scaler` to `matrix`. For example:
      
      >>> matrix = [
         [4, -7], 
         [-3, 0], 
         [-1, 1],
         [-5, -4],
      ]
      >>> result = Matrices().scaler_div(4, matrix2)
      >>> print(result)
      [[1.0, -1.75], [-0.75, 0.0], [-0.25, 0.25], [-1.25, -1.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      # Copy the 'matrix' in here.
      divided = matrix.copy()
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            value = self.set_digits(divided[i][j]/scaler, digits)
            divided[i][j] = value

      return divided

   def dot_div(self, matrix1: list[list], matrix2: list[list], 
               digits: int = 6): 
      """ Divide the 'matrix1' to 'matrix2' with each other
      as dot. If there is any zero division error, replace that 
      with 'None'. For example: 
      
      >>> matrix1 = [
         [-4, 0], 
         [6, -1], 
         [-5, 3]
      ]
      >>> matrix2 = [
         [2, 1], 
         [0, 9], 
         [8, 7]
      ]
      >>> result = Matrices().dot_div(matrix1, matrix2)
      >>> print(result)
      [[-2.0, 0.0], [None, -0.11111], [-0.625, 0.42857]]
      """
      if not self.ismatrix(matrix1) or not self.ismatrix(matrix2):
         raise MatrixError("Inconsistent matrix defination")
      if not self.dim(matrix1) == self.dim(matrix2):
         raise DimensionError("Found dimension dicrepancy")
      # Initially, generate the zeros matrix and 
      matrix = self.zeros(dim=self.dim(matrix1))
      # fill the matrix with divided elements.
      for i in range(len(matrix1)):
         for j in range(len(matrix2[0])):
            # Division operation can cause 'ZeroDivisionError'.
            try: 
               divided = matrix1[i][j] / matrix2[i][j]
            except ZeroDivisionError: # catch up the error
               matrix[i][j] = None
            else: # otherwise, continue the divison operation
               matrix[i][j] = self.set_digits(divided, digits)

      return matrix

   # ----------------------------------------------------------------
   # --------------------- Advanced Methods -------------------------
   # ----------------------------------------------------------------

   def det(self, matrix: list[list], digits: int = 6) -> float: 
      """ Calculate the determinant of `matrix`. For example:

      >>> matrix = [
         [2, 1, 4, 8], 
         [0, 9, -1, -4], 
         [8, 7, -6, 7], 
         [8, 7, 0, 0]
      ]
      >>> result = Matrices().det(matrix)
      >>> print(result)
      5286.0
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistance matrix defination")
      if not self.issquare(matrix):
         raise SquareMatrixError("'matrix' must be square")
      
      def det1(matrix, digits=digits):
         # Calculation the determinant of 1x1 matrix.
         return self.set_digits(matrix[0][0], digits)
      
      def det2(matrix, digits=digits):
      # Calculate the determinant of 2x2 matrix.
         s1 = matrix[0][0] * matrix[1][1]
         s2 = matrix[0][1] * matrix[1][0]
         return self.set_digits(s1 - s2, digits)
      
      # Put the all coefficients in here.
      self.coefs = []
      # Immediately, put the first row of 'matrix' in it.
      coef = matrix[0].copy()
      for i, el in enumerate(coef):
         if i % 2 == 1 and not el == 0:
            coef[i] = -1 * el
      self.coefs.append(list(coef))

      # The main stretagy is to generate the 2x2 sub-matrices from
      # 'matrix'. For this, required so many sub-method. First is
      # 'parse_one' which reduce the dimension for one time.
      def parse_one(matrix):
         # Reduce the dimension of 'matrix' and generate the new
         # sub-matrices.
         parsed = [] # pool the new sub-matrices in here
         for i in range(len(matrix[0])):
            copied = matrix.copy() # copy the 'matrix'
            del copied[0] # delete the first row
            tranposed = self.transpose(copied) # get transpose
            del tranposed[i] # delete i. column
            parsed.append(self.transpose(tranposed)) # get transpose 
         
         return parsed
      
      # 'parsed_one' method reduce the dimension of 'matrix' for
      # one time, and generate the new sub-matrices. But, mostly, 
      # it is not enough one time reduction. So, determine new
      # sub-method named 'parsed_more'.
      def parse_more(matrix, digits=digits):
         # Reduce the dimension of 'matrix' until generated 2x2
         # sub-matrices
         parsed = parse_one(matrix)
         # Continously, reduce the dimension of 'matrix' until
         # reaches 2x2 sub-matrices.
         for submatrix in parsed:
            parse = parse_one(submatrix)
            for m in parse:
               if len(m) == 1:
                  break
               parsed.append(m)
         # Right know, we should collect the coefficients.
         for submatrix in parsed:
            if self.dim(submatrix) >= (3, 3):
               coef = submatrix[0].copy()
               for i, el in enumerate(coef):
                  if i % 2 == 1 and not el == 0:
                     coef[i] = -1 * coef[i]
               self.coefs.append(coef)
         # Just want to calculate the determinant of 2x2 sub-
         # matrices. So limit the 'parsed'.
         index = int(len(parsed)-math.factorial(len(matrix))/2)
         parsed = parsed[index:]
         # Calculate the determinant of 2x2 sub-matrices.
         for submatrix in parsed:
            if not self.ismatrix(submatrix):
               break
            parsed.append(det2(submatrix, digits))
         # Again, limit the 'parsed'.
         parsed = parsed[int(len(parsed)/2):]

         return parsed
      
      # 'parsed_more' method has prepared the determinant of 2x2
      # sub-matrices and coefficients corresponding to dets.
      def det_more(matrix, digits):
         parsed = parse_more(matrix, digits)
         # Convert the 'parsed' array to mmatrix. For this, 
         # initially, generate the zeros matrix.
         row, dets, limit = [], [], 3
         for value in parsed:
            row.append(value)
            if len(row) == 3:
               dets.append(list(row))
               row = []
         # Lastly, calculate the determinant.
         while True:
            coefs = [coef for coef in self.coefs 
                          if len(coef) == limit]
            dot = self.dot_mul(coefs, dets, digits)
            agg = self.aggregate(dot, axis=1)
            limit += 1
            dets.clear()
            for el in agg: dets.append(el)
            if len(dets) == 1: break
            dets = self.reshape((int(len(agg)/limit), limit), agg)

         return self.set_digits(dets[0][0], digits)

      # Finally, can be completed finding process of determinant of
      # any matrix thanks to above methods.
      if self.dim(matrix) == (1, 1):
         return det1(matrix, digits)
      if self.dim(matrix) == (2, 2):
         return det2(matrix, digits)
      if self.dim(matrix) >= (3, 3):
         return det_more(matrix, digits)

   def minors(self, matrix: list[list], 
              digits: int = 6) -> list[list]: 
      """ Return minors map of `matrix`. For example: 
      
      >>> matrix = [
         [-1, 2, 3], 
         [-4, 6, 8], 
         [7, -8, 9], 
      ]
      >>> result = Matrices().minors(matrix)
      >>> print(result)
      [[118.0, -92.0, -10.0], [42.0, -30.0, -6.0], 
      [-2.0, 4.0, 2.0]]
      """
      if not self.issquare(matrix):
         raise SquareMatrixError("'matrix' must be square")
      if self.dim(matrix) == (1, 1):
         raise MinorsError("Could not extracted minors map")
      # Reduce the dimension of 'matrix' for one time.
      minors = []
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
            copied = matrix.copy()
            del copied[i]
            transposed = self.transpose(copied)
            del transposed[j]
            minors.append(self.transpose(transposed))
      # And then determinant each sub-matrix in 'minors'.
      row, minors_map = [], []
      for submatrix in minors:
         row.append(self.det(submatrix, digits))
         if len(row) == len(matrix[0]):
            minors_map.append(list(row))
            row = []

      return minors_map

   def cofactors(self, matrix: list[list], 
                 digits: int = 6) -> list[list]: 
      """ Extract the cofactors map of `matrix`. For example: 
      
      >>> matrix = [
         [-1, 2, 3], 
         [-4, 6, 8], 
         [7, -8, 9], 
      ]
      >>> result = Matrices().cofactors(matrix)
      >>> print(result)
      [[118.0, 92.0, -10.0], [-42.0, -30.0, 6.0], 
      [-2.0, -4.0, 2.0]]
      """
      if not self.issquare(matrix):
         raise SquareMatrixError("'matrix' must be square")
      if self.dim(matrix) == (1, 1):
         raise CofactorsError("Could not extracted cofactors map")
      # Can be used minors map for this.
      cofactors = self.minors(matrix, digits)
      for i in range(len(cofactors)):
         for j in range(len(cofactors[0])):
            if (i+j) % 2 == 1 and not cofactors[i][i] == 0:
               cofactors[i][j] = -1 * cofactors[i][j]

      return cofactors

   def isinvertible(self, matrix: list[list]) -> bool: 
      """ Return True, if `matrix` is invertible. """
      if self.det(matrix, 18) != 0: return True
      return False 

   def adjoint(self, matrix: list[list], 
               digits: int = 6) -> list[list]: 
      """ Extract the adjoint of `matrix`. For example:  
      
      >>> matrix = [
         [-1, 2, 3], 
         [-4, 6, 8], 
         [7, -8, 9],
      ]
      >>> result = Matrices().adjoint(matrix)
      >>> print(result)
      [[118.0, -42.0, -2.0], [92.0, -30.0, -4.0], 
      [-10.0, 6.0, 2.0]]
      """
      return self.transpose(self.cofactors(matrix, digits))
   
   def inverse(self, matrix: list[list], 
               digits: int = 6) -> list[list]: 
      """ Get the inverse of `matrix`. For example: 
      
      >>> matrix = [
         [-1, 2, 3], 
         [-4, 6, 8], 
         [7, -8, 9],
      ]
      >>> result = Matrices().inverse(matrix)
      >>> print(result)
      [[3.27777, -1.16666, -0.05555], [2.55555, -0.83333, 
      -0.11111], [-0.27777, 0.16666, 0.05555]]
      """
      if not self.isinvertible(matrix): 
         raise InvertibleMatixError("'matrix' must be invertible")
      # Calculate the determinant of 'matrix'.
      det = self.det(matrix, digits) 
      # Extract the adjoint of 'matrix'.
      adjoint = self.adjoint(matrix, digits)
      # Use 'scaler_div' method for dividing 'det' to 'adjoint'.
      inverse = self.scaler_div(det, adjoint, digits)

      return inverse

   def solve(self, matrix: list[list], 
             digits: int = 6) -> list[list]: 
      """ Solve the any linear equation systems. `matrix` must be
      augmented form. For example:

      >>> matrix = [
         [1, -2, 3, 9], 
         [-1, 3, 0, -4], 
         [2, -5, 5, 17],
      ]
      >>> result = Matrices().solve(matrix)
      >>> print(result)
      [[1.0], [-1.0], [2.0]]
      """
      if not self.ismatrix(matrix):
         raise MatrixError("Inconsistent matrix defination")
      if len(matrix[0]) - len(matrix) != 1:
         raise DimensionError("'matrix' must be augmented form")
      # Divide the 'main' into 'main' and 'target' matrices.
      row, main, target = [], [], []
      for i in range(len(matrix)):
         for j in range(len(matrix[0])-1):
            row.append(matrix[i][j])
            if len(row) == len(matrix[0]) - 1:
               main.append(list(row))
               row = []
      for i in range(len(matrix)):
         target.append([matrix[i][-1]])
      # Check if the 'main' matrix is invertible.
      if not self.isinvertible(main):
         raise InvertibleMatixError("'matrix' must be invertible")
      # Use the 'inverse' and 'cross_mul' methods in here.
      inverse = self.inverse(main, digits)
      solve = self.cross_mul(inverse, target, digits)

      return solve

