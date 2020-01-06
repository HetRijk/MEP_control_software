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

def logarithm(x, a, b, c):
    loga = a * np.log(b * x) + c
    return loga

def linear(x, a, b):
    return  a * x + b

# Inputs
    
folder = r'D:\Rijk\MEP_control_software\0106_1430_wo3196_dev2_air\data'
file_name = '0106_1430_wo3196_dev2_air_resistance'
file = os.path.join(folder, file_name)

func = linear

start   = 10
stop    = 3500

p0 = [1, 1]
#p0      = [2E7, 1E4, 2E7]
#bounds = (0, np.inf)

# Import data
data = instr.load_data(file)

xdata0 = data[0]
ydata0 = data[1] 

if start > 0:
    if stop < len(xdata0):
        xdata0 = xdata0[start:stop]
        ydata0 = ydata0[start:stop]
    else:
        print('Stop index too large for current array')
        xdata0 = xdata0[start:]
        ydata0 = ydata0[start:]
        xdata0 = xdata0 - min(xdata0)
        
else:
    print('Start index zero or lower, so not used')
    if stop < len(xdata0):
        xdata0 = xdata0[:stop]
        ydata0 = ydata0[:stop]
    else:
        print('Stop index too large for current array')
#
## Correction for logarithmic fitting purposes
##   gets rid of the negative values in y
#for i in range(len(ydata)):
#    if ydata[i] < 0.01:
#        ydata[i] = 1E9
#    else:
#        ydata[i] = ydata[i]

# Perform regular fit and constrained fit
popt, pcov = curve_fit(func, xdata0, ydata0, p0, maxfev=int(1E7))
#popt, pcov = curve_fit(func, xdata, ydata, p0, maxfev=int(1E7), bounds=bounds)

# Plot fit

plt.close('all')

plt.figure()
plt.plot(xdata0, ydata0)
plt.plot(xdata0 + start, func(xdata0, *popt))

plt.title('Resistance with source voltage %s mV' % 1000)
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

#plt.yscale('log')
#plt.yscale('linear')

plt.legend(['Data', 'Fit'])

#instr.save_plot(file_name + '_fit')

## Subtract linear part of the measurement
y_nonlin = ydata0 - func(xdata0, *popt)

# Fourier Transform of data
y_fft = np.fft.fft(y_nonlin)

fft_mag     = np.abs(y_fft)
fft_phase   = np.angle(y_fft) 

plt.figure()
plt.plot(fft_mag)

plt.xlabel('f(Hz)')
plt.title('FFT of WO3196 noise data with linear part subtracted')
plt.legend(['Magnitude'])


plt.figure()
plt.plot(fft_phase)

plt.xlabel('f(Hz)')
plt.title('FFT of WO3196 noise data with linear part subtracted')
plt.legend(['Phase'])