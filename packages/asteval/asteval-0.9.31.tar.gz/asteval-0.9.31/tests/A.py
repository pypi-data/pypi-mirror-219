from asteval import make_symbol_table, Interpreter
import math
from functools import partial
import numpy as np


def cosd(x):
    "cos with angle in degrees"
    return np.cos(np.radians(x))

def sind(x):
    "sin with angle in degrees"
    return np.sin(np.radians(x))

def tand(x):
    "tan with angle in degrees"
    return np.tan(np.radians(x))

for nested in True, False:
    sym_table = make_symbol_table(cosd=cosd, sind=sind, tand=tand,
                                  nested=nested)

    print(repr(sym_table))
#
# sym_table = make_symbol_table(sqrt=partial(math.sqrt), nested=False) #
# @ True)
# aeval = Interpreter(symtable=sym_table)
#
# assert aeval("sqrt(4)") == 2
#
# aeval("sqrt(-1)")
# print(aeval.error[0].exc)
