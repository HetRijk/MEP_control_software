# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:32:43 2020

@author: Rijk
"""

import numpy as np 
import instrument_module as instr
import matplotlib.pyplot as plt
import os

# =============================================================================
# Load data
# =============================================================================

name = 'pt_02nm_2_step'
base = r'C:\Users\Rijk\Google Drive\Master Thesis\Production\Platinum\200302 Temescal Pt test\AFM'

file = os.path.join(base, name)

data = instr.load_data(file)

xdata0 = data[0]*1E6
ydata0 = data[1]*1E9

start = 28
stop = 1000

# =============================================================================
# Crop and measure mean and std
# =============================================================================

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

mean    = np.mean(ydata)
std     = np.std(ydata)

print('Mean is %s' % mean)
print('Std is %s' % std)

ydata0 = ydata0 + min(ydata0) + 0.5

# =============================================================================
# Figures
# =============================================================================
plt.close('all')

plt.figure()
plt.plot(xdata0, ydata0)
#plt.plot(xdata, ydata)

plt.xlabel('Distance ($\mu$m)')
plt.ylabel('Surface Height (nm)')

plt.ylim([0, 3])
plt.xlim([0, 1.2])

plt.grid()