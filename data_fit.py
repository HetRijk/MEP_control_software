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
    return a * (1 - np.exp(-x/b)) + c

def logarithm(x, a, b):
    loga = a * np.log(x) + b
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
    
folder = r'C:\Users\Rijk\Documents\MEP\Literature\WO3'
file_name = 'gio_wo3_h2_figure5b_EaVsRho300K'


#file = os.path.join(folder, file_name, 'data', file_name + '_resistance')
file = os.path.join(folder, file_name)

func = logarithm

start   = 0
stop    = -1

#Ea = 310e-3

#p0 = [1E11, 1E3, 1E7]
#p0      = [2E7, 1E4, 2E7]
#bounds = ([1E1, 0, 1E1], [1E12, 1E1, 1E12]) 

# Import data
data = instr.load_data(file)

xdata0 = data[0]
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
popt, pcov = curve_fit(func, xdata, ydata, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E9))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7), bounds=bounds)

perr = np.sqrt(np.diag(pcov))

xdata = np.linspace(min(xdata), max(xdata), int(1E3))
#ydata = np.linspace(min(ydata0), max(ydata0), int(1E2))
yfit   = func(xdata, *popt)

mean    = np.mean(ydata0)
std     = np.std(ydata0)

print('Mean is %s' % mean)
print('Std is %s' % std)

# =============================================================================
# Plotting
# =============================================================================
plt.close('all')

plt.figure()
plt.plot(xdata0, ydata0, label='Measured')
plt.plot(xdata, yfit, label='Fit')
plt.plot(xdata0, 19*np.log(xdata0)+90)

plt.xlabel('t(s)')
#plt.xlabel('T (K)')
plt.ylabel('Resistance (M$\Omega$)')

plt.grid()
#plt.legend()

plt.xlim([min(xdata0), max(xdata0)])

#plt.xlim([1100, 2000])
#plt.ylim([1E-2, 1E2])
#plt.ylim([-0.5, 20])

plt.xscale('log')

data_fit = np.array([xdata, yfit])
fit_name = 'full'
#fit_name = 'fit_AirToH2'
#instr.save_data(file + '_' + fit_name, data_fit)

#instr.save_plot(os.path.join(folder, file_name + '_' + fit_name))
#instr.save_plot(os.path.join(folder, file_name + '_' + fit_name + '_log'))
