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

def negative_exponent(x, a, b, c):
    return a * np.exp(- x / b) + c

def reverse_exponent(x, a, b, c):
    return a * (1 - np.exp(-b * x)) + c

def logarithm(x, a, b, c, d):
    loga = a * np.log(b * x + d) + c
    return loga

def linear(x, a, b):
    return  a * x + b

def power_law(x, a, b, c):
    return a * x**b + c

def recovery(x, a, b, c):
    return - a * np.exp(-x /b) + c

def R_T(x, a, b, c):
    return a * (np.exp(b / (x-c)) + 1)

def serial_arrhenius(T, A, Ea, B):
    kb = 8.617333262145E-5 #eV/K
    return A * np.exp( Ea / (kb*T)) + B

def arrhenius(T, A, Ea):
    kb = 8.617333262145E-5 #eV/K
    return A * np.exp( Ea / (kb*T))

def parallel_arrhenius(T, A, Ea, B):
    R_T = arrhenius(T, A, Ea)
    return (R_T * B) / (R_T + B)

def both_arrhenius(T, A, Ea, B, C):
    R_T = arrhenius(T, A, Ea)
    Rs = R_T + C
    return (Rs * B) / (Rs + B)

def inverse(x, a, b):
    return a / (x - b)

# Inputs
    
folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200324 WO3196dev9\R_T\0327_1231_WO3196dev9_Tsteps5C_RvsT'
file_name = '0327_1231_WO3196dev9_Tsteps5C_RvsT'


#file = os.path.join(folder, file_name, 'data', file_name + '_resistance')
file = os.path.join(folder, file_name)

func = arrhenius

start   = -1
stop    = int(1E7)

Ea = 310e-3

#p0 = [1E9, 1E-3, 1E9]
#p0      = [2E7, 1E4, 2E7]
#bounds = ([1E1, 0, 1E1], [1E12, 1E1, 1E12]) 

# Import data
data = instr.load_data(file)

xdata0 = data[0] + 273.15
ydata0 = data[1]

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

# Perform regular fit and constrained fit
popt, pcov = curve_fit(func, xdata0, ydata0, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata0, ydata0, p0, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7), bounds=bounds)

perr = np.sqrt(np.diag(pcov))

# Plot fit

#plt.close('all')

xdata = np.linspace(min(xdata0), max(xdata0), int(1E2))
ydata = np.linspace(min(ydata0), max(ydata0), int(1E2))

mean    = np.mean(ydata0)
std     = np.std(ydata0)

print('Mean is %s' % mean)
print('Std is %s' % std)

# =============================================================================
# Plotting
# =============================================================================
plt.close('all')

plt.figure()
plt.plot(xdata0, ydata0)
#plt.plot(data20to50[0], data20to50[1])
plt.plot(xdata, func(xdata, *popt))
plt.plot(xdata, func(xdata, popt[0], Ea))
#plt.title('Resistance with source voltage %s mV' % 1000)
#plt.xlabel('t(s)')
#plt.ylabel('Resistance (Ohm)')

#plt.title('Resistance in H2 500ppm/0.4bar')
plt.ylabel('Resistance (Ohm)')
#plt.xlabel('t (s)')
plt.xlabel('T (K)')
plt.grid()

#plt.ylim(min(xdata0), 120)
#plt.xlim(min(ydata0), 1.2E5)
plt.title('WO3196 Device 9 R(T)')
#plt.ylim([0, 1E9])
#plt.xlim([20, 105])

#plt.yscale('log')
plt.yscale('linear')
#
#plt.xscale('log')
#plt.yscale('log')

plt.legend(['Data', 'Fit Arrhenius', '%s eV' % Ea])
#plt.legend(['40 to 100$^\circ$C', '25 to 50$^\circ$C'])

#instr.save_plot(os.path.join(folder, file_name + '_fit_arr'))
