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
meas_name = '1024_1258_wo3189_r13'

start   = 0
stop    = 500

set_temperature = 25

base = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\Measurements\WO3189'
data_type = 'resistance'
#data_type = 'temperatures'

# =============================================================================
# Code
# =============================================================================
# Create path to file
folder = 'Time constants %.2gC' % set_temperature
file = os.path.join(base, folder, meas_name, 'data', meas_name + '_' + data_type)

# Import data
data = instr.load_data(file)

xdata0 = data[0]
ydata0 = data[1] 

#start   = len(xdata0) - int(6*1E3)
#stop    = int(1E5)

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

# Pressure
plt.figure()
file_pressure = os.path.join(base, folder, meas_name, 'data', meas_name + '_pressure')
x_pressure = instr.load_data(file_pressure)[0]
y_pressure = instr.load_data(file_pressure)[1]
plt.plot(x_pressure, y_pressure)

# Resistance / Temperature
plt.figure()

if data_type == 'resistance':
    plt.plot(xdata0, ydata0*1E-6)
else:
    plt.plot(xdata0, ydata0)
#plt.plot(xdata, ydata*1E-6)

#plt.legend()
plt.grid('on')

#plt.yscale('log')

plt.xlim([min(xdata0), max(xdata0)])
#plt.ylim([1E0, 1E2])
plt.ylim([6, 12])
#if data_type == 'temperatures':
#    plt.ylim([60 + 3, 70 - 3])
plt.xlim([4400, 5000])

#plt.title('WO3189 - 1000 ppm H$_2$/Ar exposure')
plt.xlabel('t (s)')
plt.ylabel('Resistance (M$\Omega$)')
if data_type == 'temperatures':
    plt.ylabel('Celsius ($^\circ$C)')


# =============================================================================
# Save figure command
# =============================================================================
# Uncomment and run with f9, then comment out again

figure_name = 'Air_response'
if data_type == 'temperatures':
    figure_name = figure_name + '_temperature'
figure_file = os.path.join(base, meas_name) + '_' + figure_name

instr.save_plot(figure_file)

