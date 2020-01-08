# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:08:09 2019

@author: LocalAdmin

Module with functions to control Lakeshore 332 Temperature Controller thorugh a GPIB connection

"""

import visa
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

def cooldown_fun(t, tau):
    T0 = 150
    Troom = 40.82
    T = (T0-Troom)*np.exp(-t/tau) + Troom
    return T

taus    = np.linspace(10, 30, 5)

plt.figure(0)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')
labels = []
for i in range(len(taus)):
    plt.plot(times, cooldown_fun(times, taus[i]))
    labels.append('tau=%s' % taus[i])
    
plt.plot(times, temps)
labels.append('experiment')
plt.legend(labels)
