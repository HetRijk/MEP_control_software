# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 12:26:20 2019

@author: Rijk

Calculates the final mixing pressure by first calculating the volumes of unknown chambers
"""

import math as m


# TODO: Correct for inner diameter instead of inner radius
def V_corner_short(A, B):
    "A is the radius of the corner and B is the inner diameter of the tube"
    return m.pi**2 / 8 * A * B**2

def V_corner_long(A, B, C):
    """A is the distance between one end of the tube and the middle if the other end, 
    B is the length of one of the straight parts and C is the inner diameter"""
    return m.pi/2*B*C**2 + m.pi**2/8*(A-B)*C**2

def V_chamber(A, B, C):
    """A is the length of the main pipe, 
    B the distance from the middle of the main pipe to the end of the side pipe and 
    C is the inner diameter of the pipe"""
    return m.pi/4 * C**2 * (A + B - C/2)

def V_adapter(D, D2, L):
    return m.pi/8 * L * (D**2 + D2**2)

def cylinder(d, L):
    return m.pi/4 * d**2 * L

chamber_small   = V_chamber(40, 80, 16)
chamber_large   = V_chamber(65, 130, 40)

corner_short    = V_corner_short(40, 16)
corner_long     = V_corner_long(68, 42, 16) # 42 mm for B is estimated

adapter         = V_adapter(40, 16, 40)

pc_mix          = cylinder(6.5, 60) #Estimated
pc_main         = cylinder(6.5, 95) #Estimated

V_est_valve     = cylinder(14, 80)


Vair    = 2*adapter + chamber_large
Vmix    = chamber_small + 2*corner_short + corner_long + pc_mix
Vmain   = pc_main 

# Pressures in bar
P0      = 1
Pmix    = 0.78
 
Valve   = (Pmix/P0*(Vair + Vmix + Vmain) - Vair) / (2 - 3 * Pmix / P0)

print('Valve has volume of %.0f mm**3' % Valve)
print('Valve has volume of %.3f L' % (Valve*10**-6))
