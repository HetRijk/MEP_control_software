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
    
folder = r'D:\Rijk\MEP_control_software\0106_1430_wo3196_dev2_air\data'
file_name = '0106_1430_wo3196_dev2_air_resistance'
file = os.path.join(folder, file_name)

start   = 10
stop    = 3599

# Code

# Import data
data = instr.load_data(file)

xdata0 = data[0]
ydata0 = data[1] 

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
#y = np.zeros(np.shape(ydata0))
#for i in range(len(ydata0)):
#    if ydata0[i] < 0.01:
#        y[i] = 1E9
#    else:
#        y[i] = ydata0[i]

#y_smooth = smooth(ydata0, 20)

plt.figure()
plt.plot(xdata0, ydata0)
#plt.plot(xdata0, y)

#plt.yscale('log')

#plt.xlabel('t (s)')
#plt.ylabel('Resistance (Ohm)')

#plt.legend(['Original data', 'Edited'])


