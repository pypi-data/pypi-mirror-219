# Errors in ALAT (Advanced Linear Algebra Toolkit)

class MatrixError(Exception):
   """ Raise error, if given matrix is valid defination. """

class SquareMatrixError(Exception):
   """ Raise error, if given matrix is square. """

class ModeError(Exception):
   """ Raise error, if given matrix has not any mode/s. """

class DimensionError(Exception):
   """ Raise error, if there is dimension dicrepancy. """

class PointsError(Exception):
   """ Raise error, if there is points error. """

class UpperTriangularMatrix(Exception):
   """ Raise error, if there is a invalid value in the matrix. """

class LowerTriangularMatrix(Exception):
   """ Raise error, if there is a invalid value in the matrix. """

class MinorsError(Exception):
   """ Raise error, if given matrix is 1x1 dimension. """

class CofactorsError(Exception):
   """ Raise error, if given matrix is 1x1 dimension. """

class InvertibleMatixError(Exception):
   """ Raise error, if given matrix in not invertible. """

class ZeroLenghtError(Exception):
   """ Raise error, if given vector has zero lenght. """

class ZeroVectorError(Exception):
   """ Raise error, if given vector is zeros. """

class CrossMultiplicationError(Exception):
   """ Raise error, if given vectors have not 3D dimension. """

class LinearCombinationError(Exception):
   """ Raise error, there is no linear configuration. """

class PolynomialCureFittingError(Exception):
   """ Raise error, there is error. """

class InconsistentCharacterError(Exception):
   """ Raise error, there is a inconsistent character. """

class MissingCharacters(Exception):
   """ Raise error, there is the missing characters. """