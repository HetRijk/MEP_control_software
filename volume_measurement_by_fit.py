# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 18:09:32 2019

@author: Rijk

"Machine learning" appraoch to determining the volume of the SpeedyValve and the main pressure controller internals
"""

import math as m
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def V_corner_short(A, C):
    "A is the radius of the corner and B is the inner diameter of the tube"
    r = C/2
    return m.pi*r**2 * m.pi/2*A

def V_corner_long(A, B, C):
    """A is the distance between one end of the tube and the middle if the other end, 
    B is the length of one of the straight parts and C is the inner diameter"""
    return m.pi/2*B*C**2 + m.pi**2/8*(A-B)*C**2

def V_chamber(A, B, C):
    """A is the length of the main pipe, 
    B the distance from the middle of the main pipe to the end of the side pipe and 
    C is the inner diameter of the pipe"""
    r = C/2
    return m.pi * r**2 * (A + B - r)

def V_adapter(D, D2, L):
    r = D/2
    r2 = D2/2
    return m.pi/2 * L * (r**2 + r2**2)

def cylinder(d, L):
    r = d/2
    return m.pi * r**2 * L


chamber_small   = V_chamber(40, 80, 16)
chamber_large   = V_chamber(65, 130, 40)

corner_short    = V_corner_short(40, 16)
#corner_long     = V_corner_long(68, 42, 16) # 42 mm for B is estimated

adapter         = V_adapter(40, 16, 40)

pc_mix          = cylinder(6.5, 60) #Estimated
pc_main         = cylinder(6.5, 95) #Estimated

V_est_valve     = cylinder(14, 80)


Vair    = 2*adapter + chamber_large
Vmix    = chamber_small + 3*corner_short 

#Vmain   = pc_main + pc_mix

# Pressures in bar
P0      = np.array([1, 0.7, 0.5, 0.3])
Pmix    = np.array([0.79765, 0.56422, 0.40968, 0.25762])


xs = -Pmix / (2*P0 - 3*Pmix)
ys = ((Pmix - P0)*Vair + Pmix*Vmix) / (2*P0 - 3*Pmix)

def linear(x, a, b):
    return  a * x + b

func = linear

popt, pcov = curve_fit(func, P0, Pmix, maxfev=int(1E7))

plt.plot(P0, Pmix)
plt.plot(P0, func(P0, *popt))

a = popt[0]
b = popt[1]

Vpc = ( ()/() - ()/() )  /  ( ()/() - ()/())