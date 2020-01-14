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
    
folder = r'C:\Users\Rijk\Documents\MEP\Measurement setup\Other hydrogen sensor'
file_name = 'calibration_curve_v2_loglog'
file = os.path.join(folder, file_name)

func = power_law

start   = 0
stop    = 3500

p0 = [1E12, -3/2, 1E5]
#p0      = [2E7, 1E4, 2E7]
#bounds = (0, np.inf)

# Import data
data = instr.load_data(file)

xdata0 = data[1]
ydata0 = data[0] 

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
#popt, pcov = curve_fit(func, xdata0, ydata0, maxfev=int(1E9))
popt, pcov = curve_fit(func, xdata0, ydata0, p0, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7), bounds=bounds)

# Plot fit

#plt.close('all')

xdata = np.linspace(min(xdata0), max(xdata0), int(1E3))
ydata = np.linspace(min(ydata0), max(ydata0), int(1E3))

plt.figure()
plt.plot(xdata0, ydata0)
plt.plot(xdata, func(xdata, *popt))

#plt.title('Resistance with source voltage %s mV' % 1000)
#plt.xlabel('t(s)')
#plt.ylabel('Resistance (Ohm)')

plt.title('Calibration curve of 2nd hydrogen sensor: IDT SGAS701')
plt.ylabel('Concentration H2 (ppm)')
plt.xlabel('Resistance (Ohm)')

#plt.ylim(min(xdata0), 120)
#plt.xlim(min(ydata0), 1.2E5)

#plt.yscale('log')
#plt.yscale('linear')
#
plt.xscale('log')
plt.yscale('log')

plt.legend(['Data', 'Fit'])

#instr.save_plot(file_name + '_fit')