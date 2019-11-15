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
    return a * (1 - np.exp(-b * x)) + c

def logarithm(x, a, b, c):
    loga = a * np.log(b * x) + c
    return loga

def linear(x, a, b):
    return  a * x + b

# Inputs
    
folder = r'D:\Rijk\MEP_control_software\1113_1139_wo3193_r13_h2_static_30_min\data'
file = '1113_1139_wo3193_r13_h2_static_resistance'

func = linear

start   = 0
stop    = 3599

p0 = [1, 1]
#p0      = [2E7, 1E4, 2E7]

# Code
file_name = os.path.join(folder, file)

# Import data
data = instr.load_data(file_name)

xdata0 = data[0]
ydata0 = data[1] 

xdata = xdata0[start:stop] 
ydata = ydata0[start:stop]

xdata = xdata - min(xdata)

# Perform regular fit and constrained fit
#popt = np.polyfit(np.log(xdata), ydata, deg=1)
popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7))

# Plot fit
plt.close('all')

plt.plot(xdata0, ydata0)
plt.plot(xdata + start, func(xdata, *popt))

plt.legend(['Data', 'Fit'])

instr.save_plot(file_name + '_fit')

instr.save_data(file_name + '_fit_coef', popt)
instr.save_data(file_name + '_fit_cov', pcov)
instr.save_data(file_name + '_fit_data', np.array([xdata, func(xdata, *popt)]))

