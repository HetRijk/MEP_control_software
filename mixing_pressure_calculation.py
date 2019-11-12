# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 16:40:45 2019

@author: Rijk

Mixing pressure estimate

Estimated volumes:
    - Pressure controller
    - SpeedyValve
"""

import math as m

def V_corner_short(A, C):
    "A is the radius of the corner and B is the inner diameter of the tube"
    r = C/2
    return m.pi*r**2 * m.pi/2*A

def V_corner_long(A, B, C):
    """A is the distance between one end of the tube and the middle if the other end, 
    B is the length of one of the straight parts and C is the inner diameter"""
    return m.pi/2*B*C**2 + m.pi**2/8*(A-B)*C**2

def V_chamber(A, B, C):
    """A is the distance from the middle of the centre pipe to the end of the side pipe
    B is the length of the main pipe and C is the inner diameter of the pipe"""
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

Valve     = cylinder(14, 80)

P0 = 0.3


Vair    = 2*adapter + chamber_large
Vmix    = chamber_small + 3*corner_short + pc_mix
Vmain   = pc_main 

Pmix = P0 * (2*Valve + Vair) / (3*Valve + Vair + Vmix + Vmain)



