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
    
meas_name = '0116_1545_WO3196_IV_curve_test'

source_folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software'

num_points = 11

folder = os.path.join(source_folder, meas_name)

fit_folder = folder + '\\fit'
try:
    os.mkdir(fit_folder)
except:
    pass

file_name = os.path.join(source_folder, meas_name, 'data', meas_name)
                            
func = linear

#p0 = [1E12, -3/2]
#p0      = [2E7, 1E4, 2E7]
#bounds = (0, np.inf)

# =============================================================================
# # Import data
# =============================================================================
ts = instr.load_data(file_name +'_current')[0]
currents = instr.load_data(file_name +'_current')[1]
voltages = instr.load_data(file_name + '_voltage')[1]


# =============================================================================
# # Perform regular fit and constrained fit
# =============================================================================
num_ivcurves = int(np.floor(len(currents)/num_points))

res_div     = voltages/currents

res_fit = np.zeros([3, num_ivcurves])
for i in range(num_ivcurves):    
    res_mean, res_var = curve_fit(func, currents[num_points*i:num_points*(i+1) -1], voltages[num_points*i:num_points*(i+1) -1], maxfev=int(1E9))
    time_mean  = np.mean(ts[num_points*i:num_points*(i+1) -1])
    res_fit[:, i] = [time_mean, np.abs(res_mean), np.sqrt(res_var)]


#ohm_res     = np.zeros(0)
#ohm_res_curr = np.zeros(0)
#for n, i in enumerate(currents):
#    if i != 0:
#        ohm_res_curr = np.append(ohm_res_curr, i)
#        ohm_res = np.append(ohm_res, voltages[n]/i)
#    else:
#        pass
# =============================================================================
# # Plot fit
# =============================================================================

#plt.close('all')

plt.figure()
plt.plot(currents[num_points:2*num_points-1], voltages[num_points:2*num_points-1])
plt.plot(currents[num_points:2*num_points-1], func(currents[num_points:2*num_points-1], res_fit[1][1]))

plt.title('IV curve')
plt.xlabel('Current (A)')
plt.ylabel('Voltage (V)')

plt.legend(['Data', 'Fit'])

instr.save_plot(os.path.join(fit_folder, meas_name + '_secondcurveandfit'))

plt.figure()
plt.errorbar(res_fit[0], res_fit[1], yerr=res_fit[2])
plt.plot(ts[::num_points], res_div[::num_points], '*')

plt.title('Fitted resistances')


#plt.figure()
#plt.plot(ohm_res_curr, ohm_res)
#plt.plot(currents, res_mean * np.ones(len(currents)))
##plt.plot(currents, func(currents, *popt))
#
#plt.title('IV of 33MOhm with %.2e mean and %.2e std' % (res_mean, res_std))
#plt.xlabel('Source current (A)')
#plt.ylabel('Resistance (Ohm)')
#
#
#plt.legend(['V/I Resistance', 'Fit Resistance'])
#
#instr.save_plot(os.path.join(fit_folder, meas_name + '_resistances'))