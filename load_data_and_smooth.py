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

# Functions 

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

# Inputs
    
folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\Measurements\WO3189\Important ones\Time constants 65C\1031_1552_wo3189_r13_h2toair\data'
file_name = '1031_1552_wo3189_r13_h2toair_resistance'
file = os.path.join(folder, file_name)

start   = 0
stop    = 3599

p0 = [1, 1]
#p0      = [2E7, 1E4, 2E7]

# Code

# Import data
data = instr.load_data(file)

xdata0 = data[0]
ydata0 = data[1] 

y_smooth = smooth(ydata0, 20)

plt.figure()
plt.plot(xdata0, ydata0)
plt.plot(xdata0, y_smooth)

#plt.yscale('log')

plt.xlabel('t (s)')
plt.ylabel('Resistance (Ohm)')

plt.legend(['Original data', 'Smooth 20'])


