""" ALAT (Advanced Linear Algebra Toolkit) 

ALAT project was developed for calculating linear algebratic 
problems automatically. Especially, in engineering and science,
linear algebratic problems are so hot topic. So, I've decided to 
write this project. I've seperated this project into 4 parts 
mainly. First is 'Matrices' class which contain the methods 
related to matrix operations. Second is 'Vectors' class which 
contain the methods about vector operations. Third is 'Apps' 
class which contain the common applications related with linear 
algebra. Fourth is 'Crypts' which provide the cryptography 
operations in 4 step.

Of course, I may have made mistake in some methods. Please, 
contact the with me over my e-mail address.

Resource: Elementary Linear Algebra, Sixth Edition by Ron LARSON, 
David C. FALVO

Starting date: 04-07-2022
"""

__author__ = "Can Gulmez (ahmetcangulmez02@gmail.com)"
__version__ = "1.2.0"
__licence__ = "MIT License"

from .matrices import Matrices
from .vectors import Vectors
from .apps import Apps
from .crypts import Crypts

