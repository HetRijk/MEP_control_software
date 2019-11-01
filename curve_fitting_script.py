# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 17:10:35 2019

@author: LocalAdmin

Curve fitting script

"""
import os
import math as m
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import instrument_module as instr

def exponent(x, a, b, c):
    return a * np.exp(- x / b) + c

def reverse_exponent(x, a, b, c):
    return a * (1 - np.exp(- x / b)) + c

def reverse_exponent(x, a, b, c):
    return a * (1 - np.exp(-b * x)) + c

def logarithm(x, a, b, c):
    loga = a*1E7 * np.log(1E-4*b * x) + c
    return loga

def linear(x, a, b, c):
    return  -a * x + b + c

# Inputs
    
folder = r'D:\Rijk\MEP_control_software\1031_1309_wo3189_r13_airtoh2\data'
file = '1031_1309_wo3189_r13_airtoh2_resistance'

func = exponent

start   = 1190
stop    = start + 250

p0      = [2E7, 1E4, 2E7]

# Code
file_name = os.path.join(folder, file)

# Import data
data = instr.load_data(file_name)

xdata = data[0][start:stop] 
ydata = data[1][start:stop]

xdata = xdata - min(xdata)

# Perform regular fit and constrained fit
#popt = np.polyfit(np.log(xdata), ydata, deg=1)
popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7))

# Plot fit
plt.close('all')

plt.plot(xdata, ydata)
plt.plot(xdata, func(xdata, *popt))

plt.legend(['Data', 'Fit'])

instr.save_plot(file_name + '_fit')

instr.save_data(file_name + '_fit_coef', popt)
instr.save_data(file_name + '_fit_cov', pcov)
instr.save_data(file_name + '_fit_data', np.array([xdata, func(xdata, *popt)]))

