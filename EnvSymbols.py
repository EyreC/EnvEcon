import math as ma
import sympy as sp
from sympy import *

# Utility Symbols
Q, S, a, b = symbols('Q,S,a,b', real=True, positive=True)

# Budget Symbols
P = symbols('P', real=True, positive=True)
cG, cN, cGeneric = symbols('c_G, c_N, c_Gen', real=True, positive=True)
Y = symbols('Y', real=True, positive=True)

# Emissions Symbols
mu = symbols('mu', real=True, positive=True)  # eco consciousness, 0 < mu < 1
eG, eN = symbols('e_G, e_N', real=True, positive=True)  # eG and eN denote emissions per Q for green and normal delivery
e_rate = symbols('e', real=True, positive=True)  # placeholder for emissions

# friendship!
om, delta = symbols('omega,delta', real=True)
F = symbols('F', real=True)

lam = symbols('lambda', real=True)
