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
    
main_folder = r'/home/rich/Documents/MEP/MEP_control_software/'
measurement = '0106_1734_33MOhm_outside'
measured = '_' + 'resistance'
file = os.path.join(main_folder, measurement, 'data', measurement + measured)

func = linear

start   = 10
stop    = 340

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
        
# Calculate sample rate form xdata
#   assuming it is constant
sample_rate = np.round(np.mean(np.diff(xdata0)), decimals=1)**-1
freqs       = 

# Plot data
plt.close('all')

plt.figure()
plt.plot(xdata0, ydata0)

plt.title('Resistance with source voltage %s mV' % 1000)
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

#plt.yscale('log')
#plt.yscale('linear')


# Fourier Transform of data
y_fft = np.fft.fft(ydata0)

fft_mag     = np.abs(y_fft)
fft_phase   = np.angle(y_fft) 

plt.figure()
plt.plot(fft_mag)

plt.xlabel('f(Hz)')
plt.title('FFT of WO3196 noise data')
plt.legend(['Magnitude'])


plt.figure()
plt.plot(fft_phase)

plt.xlabel('f(Hz)')
plt.title('FFT of WO3196 noise data')
plt.legend(['Phase'])