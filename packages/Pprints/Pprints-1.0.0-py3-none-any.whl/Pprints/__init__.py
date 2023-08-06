#  ____   ____         _         _     _      ___  ____     __   
# |  _ \ |  _ \  _ __ (_) _ __  | |_  | |    |_ _|| __ )   / / _ 
# | |_) || |_) || '__|| || '_ \ | __| | |     | | |  _ \  | | (_)
# |  __/ |  __/ | |   | || | | || |_  | |___  | | | |_) | S | |  _ 
# |_|    |_|    |_|   |_||_| |_| \__| |_____||___||____/  | | (_)
#                                                          \_\   

"""
Pprints Library
~~~~~~~~~~~~~~~~~~~~~

The PPrints library is an auxiliary library for printing in the terminal in Farsi language and Farsi color printing written with Python language for humans.
Basic usage:

>>> from Pprints import *
>>> this = Pprint()
>>> this.print('12345 سلام رفقا')
   
:Library used in the code: arabic_reshaper, bidi
:Copyright: (c) 2023 Amin Rngbr.
:license: MIT
"""

import sys

sys.dont_write_bytecode = True

from .Ppr_class import *

this : dict = {}