from scipy.stats import beta
import matplotlib.pyplot as plt
import numpy as np

# Beta distribution generation
mode, k = 0.75, 500 # mode and concentration

a = (mode * (k-2)) + 1
b = ((1-mode) * (k-2)) + 1

random_a = beta(a, b)
random_a.rvs()  # random number
mean, var, skew, kurt = random_a.stats()  #