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
    return a * np.exp(- x / b) + c

def reverse_exponent(x, a, b, c):
    return a * (1 - np.exp(-b * x)) + c

def logarithm(x, a, b, c):
    loga = a * np.log(b * x) + c
    return loga

def linear(x, a, b):
    return  a * x + b

# Inputs
    
folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\Measurements\WO3189\Time constants 50C\1025_1722_wo3189_r13 h2 to air\data'
file = '1025_1722_wo3189_r13_resistance'

func = negative_exponent

start   = 1219
stop    = 3500

p0 = [1, 1, 1]
#p0      = [2E7, 1E4, 2E7]
#bounds = (0, np.inf)

# Code
file_name = os.path.join(folder, file)

# Import data
data = instr.load_data(file_name)

xdata0 = data[0]
ydata0 = data[1] 

xdata = xdata0[start:stop] 
ydata = ydata0[start:stop]

xdata = xdata - min(xdata)


for i in range(len(ydata)):
    if ydata[i] < 0.01:
        ydata[i] = 1E9
    else:
        ydata[i] = ydata[i]

# Perform regular fit and constrained fit
popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7), bounds=bounds)

# Plot fit

plt.close('all')

plt.figure()
plt.plot(xdata0, ydata0)
plt.plot(xdata + start, func(xdata, *popt))

plt.title('Resistance with source voltage %s mV' % 1000)
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

plt.yscale('log')
#plt.yscale('linear')

plt.legend(['Data', 'Fit'])

instr.save_plot(file_name + '_fit')

# Zoomed in on the fit
plt.figure()
plt.plot(xdata0, ydata0)
plt.plot(xdata + start, func(xdata, *popt))

plt.title('Resistance with source voltage %s mV' % 1000)
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

#plt.yscale('log')
plt.yscale('linear')
plt.xlim([start, stop])

plt.legend(['Data', 'Fit'])

instr.save_plot(file_name + '_fit_zoom')

instr.save_data(file_name + '_fit_coef', popt)
instr.save_data(file_name + '_fit_cov', pcov)
instr.save_data(file_name + '_fit_data', np.array([xdata, func(xdata, *popt)]))

