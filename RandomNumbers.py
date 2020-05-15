#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RandomNumbers.py:

RandomNumbers contains functions which generate shape parameters for certain distributions.
"""

def find_beta_shape_params(mode=0, concentration=0, mean=0, stdev=0, variance=0):
    """
    Generates shape parameters for beta distribution a and b, based on mode-concentration or mean-stdev/
    mean-variance pairs

    :param mode: Mode (peak) of beta distribution
    :param concentration: The thickness of the distribution
    :param mean: Mean (expected value) of the distribution
    :param stdev: Sqrt variance
    :param variance: stdev^2

    :return: the shape parameters a and b of beta distribution
    """

    if mean > 0 and (variance > 0 or stdev > 0):
        variance = variance if stdev==0 else stdev**2

        summa = (((1 - mean) * mean) / variance) - 1
        a = mean * summa
        b = (1 - mean) * summa
        return a, b

    elif mode > 0 and concentration > 0:
        a = (mode * (concentration - 2)) + 1
        b = ((1 - mode) * (concentration - 2)) + 1
        return a, b

    else:
        print("To find beta shape parameters, enter mode-concentration or mean-stdev/ mean-variance pairs."
              "The numbers must be positive.")


