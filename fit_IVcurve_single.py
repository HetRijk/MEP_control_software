# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:25:30 2020

@author: Rijk

Extracts the resistance from the IV curves measured

"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 17:10:35 2019

@author: LocalAdmin

Curve fitting script

"""
import os
import math as m
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import instrument_module as instr

def linear(x, a):
    return  a * x

# =============================================================================
# # Inputs
# =============================================================================
    
meas_name = '0117_1703_WO3196_full_IV_curve'

source_folder = r'D:\Rijk\MEP_control_software'

num_points = 10

folder = os.path.join(source_folder, meas_name)

fit_folder = folder + '\\fit_minus'
try:
    os.mkdir(fit_folder)
except:
    pass

file_name = os.path.join(source_folder, meas_name, 'data', meas_name)

file_current = file_name +'_current'
file_voltage = file_name + '_voltage'
                            
func = linear

start   = 17
stop    = start

#p0 = [1E12, -3/2]
#p0      = [2E7, 1E4, 2E7]
#bounds = (0, np.inf)

# =============================================================================
# # Import data
# =============================================================================
ts = instr.load_data(file_current)[0]
currents = instr.load_data(file_current)[1][101:]
voltages = instr.load_data(file_voltage)[1][101:]

stop = len(currents) - stop

if start > 0:
    if stop < len(currents):
        currents = currents[start:stop]
        voltages = voltages[start:stop]
    else:
        print('Stop index too large for current array')
        currents = currents[start:]
        voltages = voltages[start:]
        currents = currents - min(currents)
        
else:
    print('Start index zero or lower, so not used')
    if stop < len(currents):
        currents = currents[:stop]
        voltages = voltages[:stop]
    else:
        print('Stop index too large for current array')

# =============================================================================
# # Perform regular fit and constrained fit
# =============================================================================
res_mean, res_var = curve_fit(func, currents, voltages, maxfev=int(1E9))
#popt, pcov = curve_fit(func, currents, voltages, p0, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7), bounds=bounds)

res_std = np.sqrt(res_var)

ohm_res     = np.zeros(0)
ohm_res_curr = np.zeros(0)
for n, i in enumerate(currents):
    if i != 0:
        ohm_res_curr = np.append(ohm_res_curr, i)
        ohm_res = np.append(ohm_res, voltages[n]/i)
    else:
        pass
# =============================================================================
# # Plot fit
# =============================================================================

#plt.close('all')

plt.figure()
plt.plot(currents, voltages)
plt.plot(currents, func(currents, res_mean))

plt.title('IV curve of 33MOhm')
plt.xlabel('Current (A)')
plt.ylabel('Voltage (V)')

plt.legend(['Data', 'Fit'])

instr.save_plot(os.path.join(fit_folder, meas_name + '_datafit'))

plt.figure()
plt.plot(ohm_res_curr, ohm_res)
plt.plot(currents, res_mean * np.ones(len(currents)))
#plt.plot(currents, func(currents, *popt))

plt.title('IV of 33MOhm with %.2e mean and %.2e std' % (res_mean, res_std))
plt.xlabel('Source current (A)')
plt.ylabel('Resistance (Ohm)')


plt.legend(['V/I Resistance', 'Fit Resistance'])

instr.save_plot(os.path.join(fit_folder, meas_name + '_resistances'))