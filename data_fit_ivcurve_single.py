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
    
folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200220 Device 2 65 C\20200220 IV Curves'
file_name = '0220_1518_WO3196_iv_65C_h2_4point'

file_current = os.path.join(folder, file_name, 'data', file_name + '_current')
file_voltage = os.path.join(folder, file_name, 'data', file_name + '_voltage')

func = linear

num_points_iv = 31

#p0 = [1E12, -3/2, 1E5]
#p0      = [2E7, 1E4, 2E7]
#bounds = (0, np.inf)

# Import data
current_plus = instr.load_data(file_current)[1][:num_points_iv]
voltage_plus = instr.load_data(file_voltage)[1][:num_points_iv]

current_min = instr.load_data(file_current)[1][num_points_iv:]
voltage_min = instr.load_data(file_voltage)[1][num_points_iv:]

start   = 0
stop    = 32

xdata0 = current_min
ydata0 = voltage_min

if start > 0:
    if stop < len(xdata0):
        xdata = xdata0[start:stop]
        ydata = ydata0[start:stop]
    else:
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
#
## Correction for logarithmic fitting purposes
##   gets rid of the negative values in y
#for i in range(len(ydata)):
#    if ydata[i] < 0.01:
#        ydata[i] = 1E9
#    else:
#        ydata[i] = ydata[i]

# Perform regular fit and constrained fit
popt, pcov = curve_fit(func, xdata, ydata, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata0, ydata0, p0, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7), bounds=bounds)

print("Resistance fitted is %s with std %s" % (popt[0], np.sqrt(pcov[0][0])))

# =============================================================================
# # Plot fit
# =============================================================================

#plt.close('all')

xdata_fit = np.linspace(min(xdata), max(xdata), int(1E3))

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