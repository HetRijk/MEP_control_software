# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:35:52 2020

@author: Rijk

Data storage test with matlab-like method
"""

import numpy as np
import matplotlib.pyplot as plt
import os 
import scipy.io as sio

size = 100

current = np.random.rand(size)
voltage = np.random.rand(size)

iv_dict = {'voltages' : voltage,
            'currents' : current}

os.mkdir('test_data_storage')
os.chdir('test_data_storage')

sio.savemat('test_data', 
            iv_dict)