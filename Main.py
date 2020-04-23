import math as ma
import sympy as sp
from sympy import *
#init_printing()
from Engine import *
from Agent import *

    # num_agents, price, a_interval, mu_interval, income_interval, cG, cN, eG, eN, friend_interval)
print('start')
engine = Engine(2, 3, [0.3, 0.7], [0.3, 0.6], [300, 500], 100, 20, 0.01, 0.03, [0.3, 0.8], [0.3, 0.8], [1, 2])
print('finished')
engine.RunNormal(1)
print("Finished")