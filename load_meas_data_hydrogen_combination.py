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
meas_name1 = '0324_1743_WO3196dev9_H2ToAir'
meas_name2 = '0324_1814_WO3196dev9_H2ToAir'
meas_name3 = '0324_1904_WO3196dev9_H2ToAir'

start   = 0
stop    = int(1E5)

base = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200324 WO3196dev9\Hydrogen'
#data_type = 'resistance'
data_type = 'temperatures'

# =============================================================================
# Code
# =============================================================================
# Create path to file
file1 = os.path.join(base, meas_name1, 'data', meas_name1 + '_' + data_type)
file2 = os.path.join(base, meas_name2, 'data', meas_name2 + '_' + data_type)
file3 = os.path.join(base, meas_name3, 'data', meas_name3 + '_' + data_type)

# Import data
x1 = instr.load_data(file1)[0]
y1 = instr.load_data(file1)[1] 

x2 = instr.load_data(file2)[0]
y2 = instr.load_data(file2)[1] 

x3 = instr.load_data(file3)[0]
y3 = instr.load_data(file3)[1]

# Normalisation to resistance before hydrogen introduction
time_h2 = int(2/3 * len(x1)) - 50

#y1 = y1/y1[time_h2]
#y2 = y2/y2[time_h2]
#y3 = y3/y3[time_h2]

# =============================================================================
# Plotting data
# =============================================================================
plt.close('all')

plt.figure()

plt.plot(x1, y1)
plt.plot(x2, y2)
plt.plot(x3, y3)

#plt.legend()
plt.grid()

#plt.yscale('log')

plt.xlim([min(x1), max(x1)])
plt.ylim([0.925, 1.125])
if data_type == 'temperatures':
    plt.ylim([60 + 2, 70 - 2])
plt.xlim([600 - 20, 700 + 20])

#plt.title('WO3189 - 1000 ppm H$_2$/Ar exposure')
plt.xlabel('t (s)')
plt.ylabel('Resistance (a.u.)')
if data_type == 'temperatures':
    plt.ylabel('Celsius ($^\circ$C)')

# =============================================================================
# Save figure command
# =============================================================================
# Uncomment and run with f9, then comment out again

figure_name = 'temperatureAir_response_all'
if data_type == 'temperatures':
    figure_name = figure_name + '_temperature'
figure_file = os.path.join(base, meas_name1) + '_' + figure_name

instr.save_plot(figure_file)

