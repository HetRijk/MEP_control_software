# -*- coding: utf-8 -*-
"""
Created on Wed May  6 15:04:40 2020

@author: Rijk

Scipy signal sos filter toolbox test
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

plt.close('all')

b, a = signal.butter(4, 100, 'low', analog=True)
w, h = signal.freqs(b, a)

plt.figure()
plt.semilogx(w, 20 * np.log10(abs(h)))

plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(100, color='green') # cutoff frequency
#plt.show()

t = np.linspace(0, 1, 1000, False)  # 1 second
sig = np.sin(2*np.pi*10*t) + np.sin(2*np.pi*20*t)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(t, sig)
ax1.set_title('10 Hz and 20 Hz sinusoids')
ax1.axis([0, 1, -2, 2])

sos = signal.butter(10, 15, 'hp', fs=1000, output='sos')
filtered = signal.sosfilt(sos, sig)

ax2.plot(t, filtered)
ax2.set_title('After 15 Hz high-pass filter')
ax2.axis([0, 1, -2, 2])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.show()

# Compare FFT before and after
fft_before  = np.fft.fft(sig)
fft_after   = np.fft.fft(filtered)

sample_time = np.mean(np.diff(t))
f           = np.fft.fftfreq(len(t), sample_time)
half        = int(len(t)/2)
plt.figure()
plt.plot(f[1:half], fft_before[1:half], label='Original')
#plt.plot(f[1:half], fft_after[1:half], label='Filtered')
plt.legend()

## Measurement data filter
#f_axis = 1.12
#nyquist_f = f_axis
#
## Define filter
#lower_f = 0.025
#upper_f = 0.065
#bandpass_f = 2*np.pi * np.array([lower_f, upper_f]) / nyquist_f
#butter_low  = signal.butter(2, lower_f, btype='lowpass', output='sos')
#butter_high  = signal.butter(2, upper_f, btype='lowpass', output='sos')
#
#b, a = signal.butter(2, bandpass_f, btype='bandstop', output='ba')
#w, h = signal.freqz(b, a)
#
#plt.figure()
#plt.plot(w, 20 * np.log10(abs(h)))