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
meas_name   = 'wo3196_xrd'
fit_name    = 'wo3196_xrd_sto_fit'

start   = 0
stop    = -1

base = r'C:\Users\Rijk\Google Drive\Master Thesis\Production\Sample 07 LAO1 WO3196\XRD'

# =============================================================================
# Code
# =============================================================================
# Create path to file
file_meas   = os.path.join(base, meas_name) 
file_fit    = os.path.join(base, fit_name)

# Import data
x_meas = instr.load_data(file_meas)[0]
y_meas = instr.load_data(file_meas)[1]

x_fit = instr.load_data(file_fit)[0]
y_fit = instr.load_data(file_fit)[1]

# =============================================================================
# Plotting data
# =============================================================================
plt.close('all')

plt.figure()
plt.plot(x_meas, y_meas, label='Measurement')
#plt.plot(x_fit, y_fit, label='Fit')

plt.yscale('log')
#plt.xlim(min(x_meas), max(x_meas))
#plt.xlim([15, 55])
plt.xlim([46, 47])
plt.ylim([1E-1, 1E5])

plt.xlabel('$2\Theta$ (degrees)')
plt.ylabel('Intensity (cps)')

#plt.legend()
plt.grid()

#instr.save_plot(file_meas + '_secondSTOpeak')