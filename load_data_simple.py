# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:32:43 2020

@author: Rijk
"""

import numpy as np 
import instrument_module as instr
import matplotlib.pyplot as plt
import os

name = 'STO_steps_trace'
base = r'C:\Users\Rijk\Google Drive\Master Thesis\Production\Sample 01 WO3189 Pt\AFM WO3'

file = os.path.join(base, name)

data = instr.load_data(file)

x_axis = data[0]*1E6 
y_axis = data[1]*1E9 - 2.8

plt.close('all')

plt.figure()
plt.plot(x_axis, y_axis)

plt.xlabel('Distance ($\mu$m)')
plt.ylabel('Surface Height (nm)')

plt.ylim([0, 1.6])
plt.xlim([0, 1.4])

plt.grid()