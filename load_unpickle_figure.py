# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:49:49 2019

@author: LocalAdmin

Test unpickleling figures
"""
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import os

folder = r'D:\Rijk\MEP_control_software\0220_1500_WO3196_65C_highHz_airToH2\figures'
file_name = '0220_1500_WO3196_65C_highHz_h2ToAir_temperatures'
file = os.path.join(folder, file_name + '.pkl')

fig_handle = pkl.load(open(file,'rb'))
fig_handle.show()

#plt.yscale('log')
plt.yscale('linear')
#plt.ylim([1E1, 1E8])