# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 17:10:35 2019

@author: LocalAdmin

Curve fitting test file

Test with complex data which should containt negative exponential failed
    Might be due to overflow error with exponential
Test with simple linear data succeeded
"""

import math as m
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def exponent(x, a, b, c):
    return a * np.exp(b * x) + c

def linear(x, a, b):
    return  a * x + b

# Perform regular fit and constrained fit
popt, pcov = curve_fit(linear, source, current)
# popt1, pcov1 = curve_fit(func, xdata, ydata, bounds=(0, [3., 1., 0.5]))

# Plot fit
plt.plot(source, current)
plt.plot(source, linear(source, *popt))

plt.legend(['Data', 'Fit'])
