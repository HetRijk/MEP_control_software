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
rc_wo3 = 'WO3_RC_(WO3)_001_1s_exported'
rc_sto = 'WO3_RC_(STO)_001_1s_exported'

base = r'C:\Users\Rijk\Documents\MEP\Experiments\First Growth WO3\WO3_structural_characterization'

# =============================================================================
# Code
# =============================================================================
# Create path to file
file_wo3 = os.path.join(base, rc_wo3)
file_sto = os.path.join(base, rc_sto)

# Import data
data = instr.load_data(file_wo3)

x_wo3 = data[0]
y_wo3 = data[1]

data = instr.load_data(file_sto)

x_sto = data[0]
y_sto = data[1]

wo3_center = 11.91 - 0.005
sto_center = 11.37 - 5E-4

# =============================================================================
# Plotting data
# =============================================================================
plt.close('all')

plt.figure()
plt.plot(x_wo3 - wo3_center, y_wo3/max(y_wo3), label = '$WO_3$')
plt.plot(x_sto - sto_center, y_sto/max(y_sto), label = '$STO$')

plt.grid()
plt.legend()

#plt.yscale('log')
plt.xlim([-0.1, 0.1])

#plt.title('Rocking Curve WO3189')
plt.xlabel('$\Delta \omega$ (degrees)')
plt.ylabel('Intensity (a.u.)')

#instr.save_plot(file_wo3 + '_fig')

