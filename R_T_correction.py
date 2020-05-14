# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:50:02 2020

@author: Rijk

Script to correct the resistance change due to the temperature not being at the equilibirum value
Arrhenius transport model used for the resistance temperature dependance 
R = R0 exp(Ea/kbT), where R0 = A

0. Fit R(T) data to get Ea
1. Calculate R0 from R(T) data
2. Calculate new R using Arrhenius equation
3. Plot new R as a function of time

Notes:
    Use gas constant instead of Boltzmann constant, as the small kbT vlaue leads to overflow problems
"""

import os
import math as m
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import instrument_module as instr

# Constants
kelvin = 273.15
kb = 8.617343e-5 #eV/K
gasR = 8.31446261815324

def RT_arr_kb(R0, T):
    kb = 1.380649E-23
    return R0*np.exp((kb*T)**-1)

def RT_arr_gas(R0, T):
    gasR = 8.31446261815324
    return R0*np.exp((gasR*T)**-1)

# =============================================================================
# Inputs
# =============================================================================

reference_temp = 65

meas_name   = '0324_1904_WO3196dev9_H2ToAir'
Ea          = 312e-3

start   = 0
stop    = -1

base = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200324 WO3196dev9\Hydrogen'
data_type = 'temperatures'

# =============================================================================
# Laod data
# =============================================================================

# Create path to file
file_temp = os.path.join(base, meas_name, 'data', meas_name + '_' + 'temperatures')
file_res = os.path.join(base, meas_name, 'data', meas_name + '_' + 'resistance')

time = instr.load_data(file_temp)[0]
temp = instr.load_data(file_temp)[1]
res = instr.load_data(file_res)[1]

# Change temperature from Celsius to Kelvin
temp = temp + kelvin
reference_temp = reference_temp + kelvin

# =============================================================================
# Correction
# =============================================================================

# Get R0
#R0 = res * np.exp(-1/(kb*temp))
#res_cor = RT_arr_kb(res * np.exp(-1/(kb*temp)), reference_temp)

R0          = res * np.exp(-Ea/(kb*temp))
#res_cor     = res * np.exp(Ea/kb * (temp**-1 - reference_temp**-1))
res_cor     = R0 * np.exp(Ea/(kb*reference_temp))

# =============================================================================
# Plotting
# =============================================================================
plt.close('all')

# Temperature
plt.figure(1)
plt.plot(time, temp - kelvin)
plt.xlabel('t (s)')
plt.ylabel('Temperature ($^\circ$C)')
plt.grid()

# Resistance base
plt.figure(2)
plt.plot(time, res*1E-6)
plt.xlabel('t (s)')
plt.ylabel('Resistance (M$\Omega$)')
plt.ylim([2.35, 2.8])
plt.grid()

# R0
plt.figure(3)
plt.plot(time, R0)
plt.xlabel('t (s)')
plt.ylabel('R0 (Ohm)')
plt.grid()

# Resistance corrected change
plt.figure(4)
plt.plot(time, (res - res_cor)*1e-6)
plt.xlabel('t (s)')
plt.ylabel('$\Delta$R (M$\Omega$)')
plt.grid()

# Resistance corrected
plt.figure(5)
plt.plot(time, res_cor*1e-6)
plt.xlabel('t (s)')
plt.ylabel('R$_{corrected}$ (M$\Omega$)')
plt.ylim([2.35, 2.8])
plt.grid()
