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
meas_name = '0319_1815_WO3196dev7_AirToH2'

start   = 0
stop    = int(1E5)

base = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200319 WO3196dev7\Hydrogen'
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

#if start > stop:
#    print('Stop is smaller than start, so wrong input')
#    xdata = xdata0
#    ydata = ydata0
#else:
#    if start > 0:
#        if stop < len(xdata0):
#            # Case 1
#            xdata = xdata0[start:stop]
#            ydata = ydata0[start:stop]
#        else:
#            # Case 2
#            print('Stop index too large for current array')
#            xdata = xdata0[start:]
#            ydata = ydata0[start:]
#        
#    else:
#        print('Start index zero or lower, so not used')
#        if stop < len(xdata0):
#            xdata = xdata0[:stop]
#            ydata = ydata0[:stop]
#        else:
#            print('Stop index too large for current array')
#            xdata = xdata0
#            ydata = ydata0
#
#mean = np.mean(ydata)
#std  = np.std(ydata)
#
#print('Mean resistance is %s' % mean)
#print('Std resistance is %s' % std)


## Smoothing

#for i in range(1,len(ydata0)):
#    if i > 600 and i < 800:
#        if ydata0[i] < 62.5E6 or ydata0[i] > 64.8E6:
#            ydata0[i] = ydata0[i - 1]
#    else:
#        if ydata0[i] < 62.5E6 or ydata0[i] > 63.6E6:
#            ydata0[i] = ydata0[i - 1]
# =============================================================================
# Plotting data
# =============================================================================
plt.close('all')

plt.figure()

if data_type == 'resistance':
    plt.plot(xdata0, ydata0*1E-6)
else:
    plt.plot(xdata0, ydata0)

#plt.legend()
plt.grid('on')

#plt.yscale('log')

plt.xlim([min(xdata0), max(xdata0)])
#plt.ylim([62, 65])
if data_type == 'temperatures':
    plt.ylim([60 + 3, 70 - 3])
#plt.xlim([600 - 20, 700 + 20])

#plt.title('WO3189 - 1000 ppm H$_2$/Ar exposure')
plt.xlabel('t (s)')
plt.ylabel('Resistance (M$\Omega$)')
if data_type == 'temperatures':
    plt.ylabel('Celsius ($^\circ$C)')

# =============================================================================
# Save figure command
# =============================================================================
# Uncomment and run with f9, then comment out again

figure_name = 'full_nopeaks'
if data_type == 'temperatures':
    figure_name = figure_name + '_temperature'
figure_file = os.path.join(base, meas_name) + '_' + figure_name

#instr.save_plot(figure_file)

