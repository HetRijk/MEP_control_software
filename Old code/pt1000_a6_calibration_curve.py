# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:43:33 2019

@author: LocalAdmin

Plot calibration curve of LittleFuse Pt1000 A6
"""

import numpy as np
import matplotlib.pyplot as plt

kel = 273.15

# Tempature range of pt1000
x = np.linspace(-200, 600)

# Quadratic fit to calibration data from Excel
def pt1000(T):
    y = -6E-4*T**2 + 3.9197*T + 998.96
    return y

y = pt1000(x)
# Plot figure
plt.figure(0)
plt.plot(x, y)

# Points for tc332 curve
temps = np.array([-200,0,200,400,600])
points = pt1000(temps)

plt.plot(temps, points, '*')

print(str(temps+273.15))
