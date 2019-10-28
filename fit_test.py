# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 17:10:35 2019

@author: LocalAdmin

Curve fitting test file

Test with complex data which should containt negative exponential failed
    Might be due to overflow error with exponential
    Works if coefficients are first multiplied to the correct order of magnitude
Test with simple linear data succeeded
with difficult data it also works
"""
import os
import math as m
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import instrument_module as instr

def exponent(x, a, b, c):
    return a*1E7 * np.exp(-b*1E-5 * x) + c*1E7

def linear(x, a, b):
    return  -a * x + b + 3.6E4

folder = r'D:\Rijk\MEP_control_software\1021_1558_wo3189_r13 2hour\data'
file = '1021_1558_wo3189_r13_resistance'

func = exponent

file_name = os.path.join(folder, file)

# Import data
data = instr.load_data(file_name)

xdata = data[0][100:]
ydata = data[1][100:]

# Perform regular fit and constrained fit
popt, pcov = curve_fit(func, xdata, ydata)
#popt, pcov = curve_fit(exponent, xdata, ydata, bounds=(0, [2., 1500., 3.]))

# Plot fit
plt.close('all')

plt.plot(xdata, ydata)
plt.plot(xdata, func(xdata, *popt))

plt.legend(['Data', 'Fit'])

instr.save_plot(file_name + '_fit')

instr.save_data(file_name + '_fit_coef', popt)
instr.save_data(file_name + '_fit_cov', pcov)
instr.save_data(file_name + '_fit_data', np.array([xdata, func(xdata, *popt)]))

