# Some applications in ALAT (Advanced Linear Algebra Toolkit)

from .errors import (
   PointsError, 
   InvertibleMatixError,
   PolynomialCureFittingError,
)
from .matrices import Matrices

__all__ = ["Apps"]

class Apps:
   """ Some applications in ALAT. 
    
   There are so many implementations of linear algebra. In this 
   class, I offer some implementations for ALAT project. These 
   implementation are polynomial cure fitting, least squares
   regeression, finding area of triangle using determinant and
   finding volume of tetrahedron using determinant.   
   """
    
   def poly_curve_fitting(self, x_points: list, y_points: list,      
                          digits: int = 6) -> list: 
      """ Polynomial Curve Fitting

      >>> x_points = [1, 2, 3] # x axis points
      >>> y_points = [4, 0, 12] # y axis points
      >>> result = Apps().poly_curve_fitting(x_points, y_points)
      >>> print(result)
      [24.0, -28.0, 8.0]
      # It means: f(x) = 24.0 - 28.0x + 8.0x**2
      """
      # Check the parameters in proper form.
      if not isinstance(x_points, list) or \
         not isinstance(y_points, list):
         raise TypeError("'x_points' and 'y_points' must be list")
      if len(x_points) != len(y_points):
         raise PointsError("Found point/s dicrepancy")
      # Generate the new 'matrix' from x and y axis points.
      row, matrix = [], []
      for point in x_points:
         start, limit = 0, len(x_points)
         while True:
            row.append(point ** start)
            start += 1
            if start == limit:
               matrix.append(list(row))
               row = []
               break
      # Generate the 'target' matrix from 'y_points' and then
      # get the transpose ot it.
      target = Matrices().transpose([y_points])
      # Get the inverse of the 'matrix'. If any error occurs, 
      # redesign it and raise new error.
      try:
         inverse = Matrices().inverse(matrix, digits)
      except InvertibleMatixError:
         raise PolynomialCureFittingError(
            "Any polynomial curve fitting can not made"
         )
      # Multiply the 'inverse' and 'target' as cross.
      muled = Matrices().cross_mul(inverse, target, digits)
      
      return [muled[i][0] for i in range(len(muled))]
   
   def least_squares_reg(self, x_points: list, y_points: list,      
                         digits: int = 6) -> list:
      """ Least square regression 
      
      >>> x_points = [1, 2, 3, 4, 5] # x axis points
      >>> y_points = [1, 2, 4, 4, 6] # y axis points
      >>> result = Apps().least_squares_reg(x_points, y_points)
      >>> print(result)
      [-0.2, 1.2]
      # It means: f(x) = -0.2 + 1.2x
      """
      # Check the parameters are in proper form.
      if not isinstance(x_points, list) or \
         not isinstance(y_points, list):
         raise TypeError("'x_points' and 'y_points' must be list")
      if len(x_points) != len(y_points):
         raise PointsError("Found point/s dicrepancy")
      # Initially, generate the zeros matrix and then fill it.
      matrix = Matrices().ones(dim=(2, len(x_points)))
      for i in range(len(x_points)):
         matrix[1][i] = x_points[i]
      # And then, make the a few matrices operation in order.
      tmatrix = Matrices().transpose(matrix)
      target = Matrices().transpose([y_points])
      cmul1 = Matrices().cross_mul(matrix, tmatrix, digits)
      cmul2 = Matrices().cross_mul(matrix, target, digits)
      cofact = Matrices().cofactors(cmul1, digits)
      cmul3 = Matrices().cross_mul(cofact, cmul2, digits)
      smul = Matrices().scaler_mul(1/50, cmul3, digits)

      return [smul[i][0] for i in range(2)]

   def area(self, *coordinates: tuple, digits: int = 6) -> float:
      """ Find area of triangle using determinant. For example:
      
      >>> result = Apps().area((1, 0), (2, 2), (4, 3))
      >>> print(result)
      1.5
      """
      # Check if the parameters in proper form.
      for coordinate in coordinates:
         if not isinstance(coordinate, tuple):
            raise TypeError("each coordinate must be tuple")
         if len(coordinate) != 2:
            raise ValueError(
               "Each coordinate must just contain x and y points"
            )
      if len(coordinates) != 3:
         raise ValueError(
            "'coordinates' must just contain three points"
         )
      # Collect the x and y axis points in here.
      x_points = [point[0] for point in coordinates]
      y_points = [point[1] for point in coordinates]
      # Initially, generate the ones matrix and replace
      matrix = Matrices().ones(dim=(3, 3))
      # the elements with the 'x_points' and 'y_points'.
      for j in range(3):
         matrix[0][j] = x_points[j]
         matrix[1][j] = y_points[j]
      # Get the transpose of 'matrix'.
      matrix = Matrices().transpose(matrix)
      # Calculate the area using determinant.
      area = Matrices().det(matrix, digits) / 2
      area = Matrices().set_digits(area, digits)

      return -1 * area if area < 0 else area

   def volume(self, *coordinates: tuple, digits: int = 6) -> float: 
      """ Calculate the volume of tetrahedron using determinant. 
      
      >>> result = Apps().volume((0, 4, 1), (4, 0, 0), (3, 5, 2), 
                                 (2, 2, 5))
      >>> print(result)
      12.0
      """
      # Check if the parameters in proper form.
      for coordinate in coordinates:
         if not isinstance(coordinate, tuple):
            raise TypeError("each coordinate must be tuple")
         if len(coordinate) != 3:
            raise ValueError(
               "Each coordinate must just contain x, y and z points"
            )
      if len(coordinates) != 4:
         raise ValueError(
            "'coordinates' must just contain four points"
         )
      # Collect the x, y and z axis points in here.
      x_points = [point[0] for point in coordinates]
      y_points = [point[1] for point in coordinates]
      z_points = [point[2] for point in coordinates]
      # Initially, generate the ones matrix and replace the
      matrix = Matrices().ones(dim=(4, 4))
      # elements with the 'x_points', 'y_points' and 'z_points'.
      for j in range(4):
         matrix[0][j] = x_points[j]
         matrix[1][j] = y_points[j]
         matrix[2][j] = z_points[j]
      # Get the transpose of 'matrix'.
      matrix = Matrices().transpose(matrix)
      # Calculate the volume using determinant.
      volume = Matrices().det(matrix, digits) / 6
      volume = Matrices().set_digits(volume, digits)

      return -1 * volume if volume < 0 else volume

