# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:38:38 2020

@author: Rijk

Solve for sheet resistance using VanderPauw method
"""

import numpy as np
import math as m

from sympy.solvers import solve
from sympy import Symbol

from scipy.optimize import fsolve

def vdP(Rs):
    Rh = 46.61
    Rv = 43.95
    return m.e**(-m.pi*Rv/Rs) + m.e**(-m.pi*Rh/Rs) - 1

Rh = 46.61
Rv = 43.95

#Rs = Symbol('Rs')
#solution = solve(vdP(Rv, Rh, Rs), Rs)

solution = fsolve(vdP, 200)

print(solution)
