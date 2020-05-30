# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:57:03 2020

@author: Rijk
"""

import numpy as np 
import matplotlib.pyplot as plt

x = 1 - np.linspace(1E-5, 1-1E-5, int(1E5))

plt.plot(x)
#plt.yscale('log')