# Cryptography methods in ALAT (Advanced Linear Algebra Toolkit)

from .errors import (
   InconsistentCharacterError,
   InvertibleMatixError,
)
from .matrices import Matrices

__all__ = ["Crypts"]

ALL_CHARS = {
   "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, 
   "8": 8, "9": 9, 

   "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16,   
   "H": 17, "I": 18, "J": 19, "K": 20, "L": 21, "M": 22, "N": 23,   
   "O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29, "U": 30,   
   "V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35, "a": 36, "b": 37, 
   "c": 38, "d": 39, "e": 40, "f": 41, "g": 42, "h": 43, "i": 44, 
   "j": 45, "k": 46, "l": 47, "m": 48, "n": 49, "o": 50, "p": 51, 
   "q": 52, "r": 53, "s": 54, "t": 55, "u": 56, "v": 57, "w": 58, 
   "x": 59, "y": 60, "z": 61, 

   "é": 62, "!": 63, "'": 64, "^": 65, "+": 66, "%": 67, "&": 68, 
   "/": 69, "(": 70, ")": 71, "=": 72, "?": 73, "_": 74, ";": 75, 
   ":": 76, "\"": 77, ">": 78, "<": 79, "|": 80, "#": 81, "$": 82, 
   "{": 83, "[": 84, "]": 85, "}": 86, "*": 87, "\\": 88, "-": 89, 
   "@": 90, "€": 91, "~": 92, ",": 93, "`": 94, ".": 95, " ": 96,
}

class Crypts:
   """ Cryptography methods in ALAT. 
   
   This class provide four basics methods for cryptography. First
   is that 'convert the message to matrix'. Second is that 'encode
   the message into a matrix'. Third is that 'decode the encoded 
   matrix'. And lastly, 'convert the encoded matrix to message'.
   """

   def to_matrix(self, message: str, dim: tuple):
      """ Convert the `message` to matrix whixh has `dim` dimension.
      If there is missing elements, in this case, fill the missing 
      elements with -1. For example: 

      >>> message = "What is going on here !!!"
      >>> result = Crypts().to_matrix(message=message, dim=(6, 6))
      >>> for row in result:
      ...   print(row)
      [32, 43, 36, 55, 96, 44]
      [54, 96, 42, 50, 44, 49]
      [42, 96, 50, 49, 96, 43]
      [40, 53, 40, 96, 63, 63]
      [63, -1, -1, -1, -1, -1]
      [-1, -1, -1, -1, -1, -1]
      """
      if not isinstance(message, str):
         raise TypeError("'message' must be string")
      if not isinstance(dim, tuple):
         raise TypeError("'dim' must be tuple")
      if len(dim) != 2:
         raise ValueError(
            "'dim' can just contain row and column info"
         )
      if dim[0] != dim[1]:
         raise ValueError(
            "Matrix that will be generated must be square"
         )
      # Generate the matrix from scratch.
      array = []
      # Find the id corresponding to characters.
      for char in message:
         if char in ALL_CHARS.keys():
            array.append(ALL_CHARS[char])
         else: # otherwise, raise error
            error_msg = "Inconsistent character: '%s'" % char
            raise InconsistentCharacterError(error_msg)
      # Convert the 'array' to 'matrix'.
      matrix = Matrices().arbitrary(-1, dim)
      index = 0
      for i in range(dim[0]):
         for j in range(dim[1]):
            # Make integer the elements of 'matrix'.
            matrix[i][j] = int(matrix[i][j])
            # Copy the 'array' elements into 'matrix'.
            if index != len(array):
               matrix[i][j] = array[index]
               index += 1
      
      return matrix
   
   def encode(self, message: str, enocding_matrix: list[list], 
              digits: int = 6):
      """ Encode the `message` using `encoding_matrix`. An important
      point is that `encoding_matrix` must be invertible. For example:
      
      >>> message = "What is going on here !!!"
      >>> encoding_matrix = [
         [1, 7, -4, -5, 1, 2],
         [-2, 0, 0, -3, 0, 1],
         [1, 0, -4, 0, -1, 9],
         [2, -8, 8, 0, 1, -8],
         [-1, -7, 4, 5, 0, 4],
         [1, 7, 4, -5, 6, -2],
      ]
      >>> result = Crypts().encode(message, encoding_matrix)
      >>> for row in result:
      ...   print(row)
      [40.0, -580.0, 728.0, -29.0, 315.0, 287.0]
      [9.0, 13.0, 388.0, -583.0, 356.0, 260.0]
      [-55.0, -469.0, 580.0, -233.0, 299.0, 536.0]
      [166.0, -488.0, 952.0, -359.0, 474.0, -149.0]
      [62.0, 449.0, -264.0, -312.0, 57.0, 122.0]
      [-2.0, 1.0, -8.0, 8.0, -7.0, -6.0]
      """
      if not Matrices().isinvertible(enocding_matrix):
         raise InvertibleMatixError(
            "'encoding_matrix' must be invertible"
         )
      # Get the dimension of 'encoding_matrix'.
      dim = Matrices().dim(enocding_matrix)
      # Convert the 'message' to 'matrix'.
      matrix = self.to_matrix(message, dim)
      # Multiply the 'matrix' and 'encoding_matrix' as cross.
      encode = Matrices().cross_mul(matrix, enocding_matrix, digits)

      return encode

   def decode(self, encoded_msg: list[list], 
              encoding_matrix: list[list], digis: int = 6):
      """ Decode the encoded message using `encoding_matrix`. An 
      important point is that `encoding_matrix` must be invertible.
      For example: 

      >>> encoded_msg = [
         [40.0, -580.0, 728.0, -29.0, 315.0, 287.0],
         [9.0, 13.0, 388.0, -583.0, 356.0, 260.0],
         [-55.0, -469.0, 580.0, -233.0, 299.0, 536.0],
         [166.0, -488.0, 952.0, -359.0, 474.0, -149.0],
         [62.0, 449.0, -264.0, -312.0, 57.0, 122.0],
         [-2.0, 1.0, -8.0, 8.0, -7.0, -6.0],
      ]
      >>> encoding_matrix = [
         [1, 7, -4, -5, 1, 2],
         [-2, 0, 0, -3, 0, 1],
         [1, 0, -4, 0, -1, 9],
         [2, -8, 8, 0, 1, -8],
         [-1, -7, 4, 5, 0, 4],
         [1, 7, 4, -5, 6, -2],
      ]
      >>> result = Crypts().decode(encoded_msg, encoding_matrix)
      >>> for row in result:
      ...   print(row)
      [32, 43, 36, 55, 96, 44]
      [54, 96, 42, 50, 44, 49]
      [42, 96, 50, 49, 96, 43]
      [40, 53, 40, 96, 63, 63]
      [63, -1, -1, -1, -1, -1]
      [-1, -1, -1, -1, -1, -1]
      """
      if not Matrices().ismatrix(encoded_msg):
         raise Matrices("Inconsistent matrix defination")
      if not Matrices().isinvertible(encoding_matrix):
         raise InvertibleMatixError(
            "'encoding_matrix' must be invertible"
         )
      # Reverse the 'encoding_matrix'.
      inverse = Matrices().inverse(encoding_matrix, digis)
      # Multiply the 'inv' and 'encoded_msg'.
      decode = Matrices().cross_mul(encoded_msg, inverse, digis)
      # And lastly, round the elements of 'decode'.
      for i in range(len(encoding_matrix)):
         for j in range(len(encoding_matrix[0])):
            decode[i][j] = round(decode[i][j])

      return decode
   
   def to_message(self, encoded_msg: list[list], 
                  encoding_matrix: list[list], digis: int = 6):
      """ Convert the encoded matrix to message. An important point
      is that `encoding_matrix` must be invertible. For example:

      >>> encoded_msg = [
         [40.0, -580.0, 728.0, -29.0, 315.0, 287.0],
         [9.0, 13.0, 388.0, -583.0, 356.0, 260.0],
         [-55.0, -469.0, 580.0, -233.0, 299.0, 536.0],
         [166.0, -488.0, 952.0, -359.0, 474.0, -149.0],
         [62.0, 449.0, -264.0, -312.0, 57.0, 122.0],
         [-2.0, 1.0, -8.0, 8.0, -7.0, -6.0],
      ]
      >>> encoding_matrix = [
         [1, 7, -4, -5, 1, 2],
         [-2, 0, 0, -3, 0, 1],
         [1, 0, -4, 0, -1, 9],
         [2, -8, 8, 0, 1, -8],
         [-1, -7, 4, 5, 0, 4],
         [1, 7, 4, -5, 6, -2],
      ]
      >>> result = Crypts().to_message(encoded_msg, encoding_matrix)
      >>> print(result)
      "What is going on here !!!"
      """
      # Decode the encoded message to raw matrix.
      decode = self.decode(encoded_msg, encoding_matrix, digis)
      # Repalce the key and value of 'ALL_CHARS'.
      all_chars = {}
      for key, value in ALL_CHARS.items():
         all_chars[value] = key
      # Find the characters corresponding to numbers.
      message = ""
      for row in decode:
         for number in row:
            if number != -1:
               message += all_chars[number]

      return message

