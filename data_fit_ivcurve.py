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
    return a * np.exp(- x / b)

def reverse_exponent(x, a, b, c):
    return a * (1 - np.exp(-b * x)) + c

def logarithm(x, a, b, c, d):
    loga = a * np.log(b * x + d) + c
    return loga

def linear(x, a, b):
    return  a * x + b

def power_law(x, a, b, c):
    return a * x**b + c

# Inputs
    
folder = r'D:\Rijk\MEP_control_software'
file_name = '0117_1703_WO3196_full_IV_curve'

file_current = os.path.join(folder, file_name, 'data', file_name + '_current')
file_voltage = os.path.join(folder, file_name, 'data', file_name + '_voltage')

func = linear

start   = 17
stop    = 101 - 17

#p0 = [1E12, -3/2, 1E5]
#p0      = [2E7, 1E4, 2E7]
#bounds = (0, np.inf)

# Import data
current_plus = instr.load_data(file_current)[1][:101]
voltage_plus = instr.load_data(file_voltage)[1][:101]


current_min = instr.load_data(file_current)[1][101:]
voltage_min = instr.load_data(file_voltage)[1][101:]

xdata0 = current_plus
ydata0 = voltage_plus

if start > 0:
    if stop < len(xdata0):
        xdata0 = xdata0[start:stop]
        ydata0 = ydata0[start:stop]
    else:
        print('Stop index too large for current array')
        xdata0 = xdata0[start:]
        ydata0 = ydata0[start:]
        xdata0 = xdata0 - min(xdata0)
        
else:
    print('Start index zero or lower, so not used')
    if stop < len(xdata0):
        xdata0 = xdata0[:stop]
        ydata0 = ydata0[:stop]
    else:
        print('Stop index too large for current array')
#
## Correction for logarithmic fitting purposes
##   gets rid of the negative values in y
#for i in range(len(ydata)):
#    if ydata[i] < 0.01:
#        ydata[i] = 1E9
#    else:
#        ydata[i] = ydata[i]

# Perform regular fit and constrained fit
popt, pcov = curve_fit(func, xdata0, ydata0, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata0, ydata0, p0, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7), bounds=bounds)

# Plot fit

#plt.close('all')

xdata_fit = np.linspace(min(xdata0), max(xdata0), int(1E3))

plt.figure()
plt.plot(xdata0, ydata0)
plt.plot(xdata_fit, func(xdata_fit, *popt))
#plt.plot(current_plus, voltage_plus)
#plt.plot(current_min, voltage_min)


plt.title('IV curve of WO3916')
plt.xlabel('Current (A)')
plt.ylabel('Voltage (V)')

#plt.ylim(min(xdata0), 120)
#plt.xlim(min(ydata0), 1.2E5)

#plt.yscale('log')
#plt.yscale('linear')
#
#plt.xscale('log')
#plt.yscale('log')

plt.legend(['Data', 'Fit'])
#plt.legend(['Plus', 'Minus'])

#instr.save_plot(file_name + '_fit')