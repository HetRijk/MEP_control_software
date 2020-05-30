# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:01:17 2020

@author: Rijk

Plot resistance data of different devices
"""

import numpy as np
import matplotlib.pyplot as plt
import os

import instrument_module as instr

# =============================================================================
# Loading data
# =============================================================================

file_name = 'Hydrogen measurements overview device 1479'
folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\Measurements'

file = os.path.join(folder, file_name)

data = instr.load_data(file).transpose()


device      = data[:, 0]
measurement = data[:, 1]
resistance  = data[:, 2:8]
area        = data[:, 8]
perimeter   = data[:, 9]

file_name_rho = 'Wo3196_dev1279_rho300K'

file_rho = os.path.join(folder, file_name_rho)

data_rho = instr.load_data(file_rho).transpose()

rho      = data_rho[:, 1]

# =============================================================================
# Calculations
# =============================================================================

# Relative resistance drop
r_air = resistance[:, 0]
r_h2  = resistance[:, 2]

rel_drop = (r_air - r_h2) / r_air * 100



# =============================================================================
# Figures
# =============================================================================

plt.close('all')

# Resistance versus perimeter
plt.figure()
plt.plot(perimeter[::2], rho, 'o', color='tab:orange', label='Air')
plt.grid()
#plt.legend(loc='center right')

plt.xlabel('Pt Perimeter ($\mu$m)')
#plt.ylabel('Resistance (M$\Omega$)')
plt.ylabel('Resistivy ($\Omega$ cm)')

plt.xlim([0, 2000])
plt.ylim([0, 16])

plot_name1      = 'RhoVsPerimeter_dev1279'
instr.save_plot(os.path.join(folder, plot_name1))


 # Resistance versus Area
plt.figure()
plt.plot(area[::2], rho, 'o', color='tab:orange', label='Air')

plt.grid()
#plt.legend(loc='center right')

plt.xlabel('Pt Area ($\mu$m$^2$)')
plt.ylabel('Resistivy ($\Omega$ cm)')

plt.xlim([0, 11000])
plt.ylim([0, 16])

plot_name2      = 'RhoVsArea_dev1279'
instr.save_plot(os.path.join(folder, plot_name2))

# Resistance drop versus perimeter
plt.figure()
plt.plot(perimeter[::2], rel_drop[::2], 'o', color='tab:orange', label='Air - H$_2$')
plt.plot(perimeter[1::2], rel_drop[1::2], 'o', label='$H_2$ - Air')


plt.grid()
plt.legend(loc='lower right')

plt.xlabel('Pt Perimeter ($\mu$m)')
plt.ylabel('Relative Resistance Drop (%)')

plt.xlim([0, 2000])
plt.ylim([0, 10])

plot_name3      = 'DRvsPerimeter_dev1279'
instr.save_plot(os.path.join(folder, plot_name3))

# Resistance drop versus area
plt.figure()
plt.plot(area[::2], rel_drop[::2], 'o', color='tab:orange', label='Air - H$_2$')
plt.plot(area[1::2], rel_drop[1::2], 'o', label='$H_2$ - Air')


plt.grid()
plt.legend(loc='lower right')

plt.xlabel('Pt Area ($\mu$m$^2$)')
plt.ylabel('Relative Resistance Drop (%)')

plt.xlim([0, 11000])
plt.ylim([0, 10])

plot_name4      = 'DRvsArea_dev1279'
instr.save_plot(os.path.join(folder, plot_name4))
