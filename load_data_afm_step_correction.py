# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:32:43 2020

@author: Rijk
"""

import numpy as np 
import instrument_module as instr
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit

def linear(x, a, b):
    return  a * x + b

# =============================================================================
# Load data
# =============================================================================

name = 'WO3196_LAO_step'
base = r'C:\Users\Rijk\Google Drive\Master Thesis\Production\Sample 07 LAO1 WO3196\AFM\LAO Step Height After WO3'

file = os.path.join(base, name)

data = instr.load_data(file)

x_axis = data[0]*1E6 
y_axis = data[1]*1E9

start = 100
stop = len(x_axis) - 1

# =============================================================================
# Fitting
# =============================================================================
xdata0 = x_axis
ydata0 = y_axis

# Select fitting range
if start > stop:
    print('Stop is smaller than start, so wrong input')
    xdata = xdata0
    ydata = ydata0
else:
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

del xdata0, ydata0

popt, pcov = curve_fit(linear, xdata, ydata, maxfev=int(1E9))

y_cor   = y_axis - linear(x_axis, *popt)
y_cor   = y_cor - min(y_cor) + 0.5
# =============================================================================
# Figures
# =============================================================================
plt.close('all')

plt.figure()
plt.plot(x_axis, y_axis, label = 'Original')
plt.plot(xdata, linear(xdata, *popt), label = 'Fit')

plt.xlabel('Distance ($\mu$m)')
plt.ylabel('Surface Height (nm)')

#plt.ylim([0, 1.6])
#plt.xlim([0, 1.4])

plt.legend()
plt.grid()


plt.figure()
plt.plot(x_axis, y_cor, label = 'Corrected')

plt.xlabel('Distance ($\mu$m)')
plt.ylabel('Surface Height (nm)')

plt.ylim([0, 26])
plt.xlim([0, 3])

#plt.legend()
plt.grid()