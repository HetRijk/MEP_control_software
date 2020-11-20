# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:50:02 2020

@author: Rijk

Script to correct the resistance change due to the temperature not being at the equilibirum value using FFT to filter out the 'wobble'
"""

import os
import math as m
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import instrument_module as instr
from scipy import signal

def gauss_mu(x, mu, sigma):
    return (sigma*np.sqrt(2*np.pi))**-1 * np.exp((-0.5*((x-mu)**2/sigma)))

def gauss_a(x, a, b, c):
    # A: height peak, B:center peak, C:Width peak
    return a*np.exp(-(x-b)**2/(2*c**2))

def db(fft):
    return 20*np.log10(np.abs(fft))
    
    
# Constants
kelvin = 273.15


# =============================================================================
# Inputs
# =============================================================================

meas_name   = '0324_1904_WO3196dev9_H2ToAir'
Ea          = 312e-3

start   = int(1E3)
stop    = 2000

base = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200324 WO3196dev9\Hydrogen'

# =============================================================================
# Load data
# =============================================================================

folder = os.path.join(base, meas_name)

# Create folder for all timeshift correction made for this measurement
folder_correction = folder + '\\correction_dt'
try:
    os.mkdir(folder_correction)
except:
    pass

# Create path to file
file_temp = os.path.join(base, meas_name, 'data', meas_name + '_' + 'temperatures')
file_res = os.path.join(base, meas_name, 'data', meas_name + '_' + 'resistance')

time = instr.load_data(file_temp)[0][start:stop]
time = time - time[0]
temp = instr.load_data(file_temp)[1][start:stop]
res = instr.load_data(file_res)[1][start:stop]

# Change temperature from Celsius to Kelvin
temp = temp + kelvin

# =============================================================================
# FFT
# =============================================================================
half = int(len(time)/2)

# Convert time shift from seconds to index
sample_time = np.mean(np.diff(time))
sample_rate = sample_time**-1

# Frequency axis for plotting
f_axis_full = np.fft.fftfreq(len(temp), sample_time)
f_axis = f_axis_full[:half]

fft_temp = np.fft.fft(temp)
fft_res = np.fft.fft(res)

ifft_temp = np.fft.ifft(fft_temp)

# =============================================================================
# "Filtering"
# =============================================================================

nyquist_f = max(f_axis)

# Define filter
lower_f = 0.025
upper_f = 0.065
bandpass_f = np.array([lower_f, upper_f])

butter_filter   = signal.butter(4, lower_f, btype='lowpass', output='sos', fs=sample_rate)
b, a            = signal.butter(4, lower_f, btype='lowpass', output='ba', fs=sample_rate)

w, h        = signal.freqz(b, a)

temp_cor    = signal.sosfilt(butter_filter, temp)
res_cor     = signal.sosfilt(butter_filter, res)

fft_temp_cor = np.fft.fft(temp_cor)
fft_res_cor  = np.fft.fft(res_cor)   

#temp_cor = np.fft.ifft(temp_fft_cor*np.exp(-1j*temp_fft_angle))
# =============================================================================
# Plotting
# =============================================================================
plt.close('all')

# Temperature with correction
plt.figure(1)
plt.plot(time, temp - kelvin, label='Original')
plt.plot(time, temp_cor - kelvin, label = 'Filtered')
plt.xlabel('t (s)')
plt.ylabel('Temperature ($^\circ$C)')
plt.title('Temperature (time)')
plt.legend()
plt.grid()

# Resistance with correction
plt.figure(2)
plt.plot(time, res*1E-6, label='Original')
plt.plot(time, res_cor*1E-6, label='Filtered')
plt.xlabel('t (s)')
plt.ylabel('Resistance (M$\Omega$)')
plt.title('Resistance (time)')
plt.legend()
plt.grid()


# Temperature FFT with filtered 
plt.figure(3)
plt.plot(f_axis[1:], db(fft_temp[1:half]), label='Original')
#plt.plot(f_axis[1:], db(fft_temp_cor[1:half]), label='Filtered')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.legend(['Original', 'Result'])
plt.title('Temperature FFT')
#plt.xlim([0, f_axis[200]])
plt.legend()
plt.grid()

# Resistance FFT
plt.figure(4)
plt.plot(f_axis[1:], db(fft_res[1:half]), label='Original')
plt.plot(f_axis[1:], db(fft_res_cor[1:half]), label='Filtered')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.title('Resistance FFT')
plt.xlim([0, f_axis[200]])
plt.legend()
plt.grid()

# Filter response
plt.figure(5)
plt.plot(w, db(h))
plt.title('Filter')
plt.ylabel('Transmission (dB)')
plt.xlabel('Frequency (Hz)')
plt.title('Filter Response')
plt.xlim([0, f_axis[200]])
#plt.xlim([0, 0.1])
plt.ylim([-100, 10])
plt.legend()
plt.grid()


