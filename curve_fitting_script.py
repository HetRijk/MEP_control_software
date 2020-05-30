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

def negative_exponent(x, a, b, c):
    return a*1E7 * np.exp(- x / (b*1E-5)) + c*1E7

def reverse_exponent(x, a, b, c):
    return a * (1 - np.exp(-b * x)) + c

def logarithm(x, a, b, c):
    loga = a * np.log(b * x) + c
    return loga

def linear(x, a, b):
    return  a * x + b

# Inputs
    
folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\Measurements\WO3189\Time constants 25C\1024_1258_wo3189_r13\data'
file_name = '1024_1258_wo3189_r13_resistance'
file = os.path.join(folder, file_name)

func = negative_exponent

start   = 1188
stop    = 1800

p0 = [1E4, 1E2, 1E-1]
#p0      = [2E7, 1E4, 2E7]
#bounds = (0, np.inf)

# Import data
data = instr.load_data(file)

xdata0 = data[0]
ydata0 = data[1] 

if start > stop:
    print('Stop is smaller than start, so wrong input')
    xdata = xdata0
    ydata = ydata0
else:
    if start > 0:
        if stop < len(xdata0):
            # Case 1
            xdata = xdata0[start:stop]
            ydata = ydata0[start:stop]
        else:
            # Case 2
            print('Stop index too large for current array')
            xdata = xdata0[start:]
            ydata = ydata0[start:]
        
    else:
        print('Start index zero or lower, so not used')
        if stop < len(xdata0):
            xdata = xdata0[:stop]
            ydata = ydata0[:stop]
        else:
            print('Stop index too large for current array')
            xdata = xdata0
            ydata = ydata0

# Perform regular fit and constrained fit
            popt, pcov = curve_fit(func, xdata, ydata, maxfev=int(1E9))
popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E9), bounds=bounds)

# Plot fit

plt.close('all')

plt.figure()
plt.plot(xdata0, ydata0)
plt.plot(xdata, func(xdata, *popt))

plt.title('Resistance with source voltage %s mV' % 1000)
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

#plt.yscale('log')
#plt.yscale('linear')

plt.legend(['Data', 'Fit'])

