# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 17:29:44 2019

@author: LocalAdmin
"""

import numpy as np

l1 = 7.5
l2 = 2.7
r = 1.7

V = np.pi*r**2*(l1+l2)

print('Small volume is %s' % V)

l1 = 13
l2 = 4.3
r = 3.9

V = np.pi*r**2*(l1+l2)

print('Large volume is %s' % V)