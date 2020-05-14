# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:27:02 2019

@author: Rijk

Script to load x,y data from .csv measurement file
"""

import numpy as np
import matplotlib.pyplot as plt
import os

import instrument_module as instr

# Inputs
meas_name = '0327_1231_WO3196dev9_Tsteps5C_correcterSource'

start   = 0
stop    = 500

base = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200324 WO3196dev9\R_T'
data_type = 'resistance'
#data_type = 'temperatures'

# =============================================================================
# Code
# =============================================================================
# Create path to file
file = os.path.join(base, meas_name, 'data', meas_name + '_' + data_type)

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

mean = np.mean(ydata)
std  = np.std(ydata)

print('Mean resistance is %s' % mean)
print('Std resistance is %s' % std)

# =============================================================================
# Plotting data
# =============================================================================
plt.close('all')
plt.figure()
plt.plot(xdata0, ydata0)
plt.plot(xdata, ydata)
plt.grid()

#plt.yscale('log')

plt.xlabel('t (s)')
plt.ylabel('Resistance (Ohm)')
plt.legend(['Original', 'Cropped'])



