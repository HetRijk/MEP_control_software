# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:49:49 2019

@author: LocalAdmin

Test unpickleling figures
"""
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt

file = r'D:/Rijk/MEP_control_software/1024_1258_wo3189_r13/figures/1024_1258_wo3189_r13_pressure.pkl'

plt.figure(2)
fig_handle = pkl.load(open(file,'rb'))
fig_handle.show()
