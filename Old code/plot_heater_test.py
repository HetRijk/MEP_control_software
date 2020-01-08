# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:50:47 2019

@author: LocalAdmin
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf

plt.close('all')

times_med1 = temps_med[1::2]
times_med1 = times_med1 - min(times_med1)
temps_med1 = temps_med[::2]

plt.figure(0)
plt.plot(times_med1, temps_med1)

times_low1 = temps_low[1::2]
times_low1 = times_low1 - min(times_low1)
temps_low1 = temps_low[::2]


plt.figure(1)
plt.plot(times_low1, temps_low1)
