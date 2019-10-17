# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:14:28 2019

@author: LocalAdmin
"""

import pickle as pkl 
import numpy as np

file_name = 'test'

x = np.linspace(0, 50)

f = open(file_name + '.pkl', 'wb')
pkl.dump(x, f)
f.close

del x

f = open(file_name + '.pkl', 'rb')
x = pkl.load(f)
f.close

print(x)