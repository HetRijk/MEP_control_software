# -*- coding: utf-8 -*-
"""
Created on Fri May  8 16:54:11 2020

@author: Rijk
"""

import numpy as np
import matplotlib.pyplot as plt
   

def ft_stepexp(w, a):
    return np.sqrt(2*np.pi)**-1 / (a + 1j*w)

def ft_step(w):
    # Ignoring the delta function
    return np.sqrt(2*np.pi)/(1j*w)

w = np.linspace(-10, 10, int(1E3))

ft = ft_step(w) - ft_stepexp(w, 1)

plt.close('all')

plt.figure()
plt.plot(w, 20*np.log10(np.abs(ft)))
plt.title('Magnitude')

plt.figure()
plt.plot(w, np.angle(ft))
plt.title('Angle')

# Stepfunction
def response(x):
    return 1- np.e**(-x)

x = np.linspace (-10, 10, int(1E3))
y = np.zeros(len(x))
for i in range(len(x)):
    if x[i] > 0:
        y[i] = response(x[i])
    else:
        pass
   
plt.figure()
plt.plot(x, y)

plt.figure()
plt.plot(w[int(1E3/2)+1:], 20*np.log10(np.abs(np.fft.fft(y)))[1:int(1E3/2)])