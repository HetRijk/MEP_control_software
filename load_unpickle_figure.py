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

folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200324 WO3196dev9\Hydrogen\0324_1904_WO3196dev9_H2ToAir\figures'
file_name = '0324_1904_WO3196dev9_H2ToAir_resistance'
file = os.path.join(folder, file_name + '.pkl')

fig_handle = pkl.load(open(file,'rb'))
fig_handle.show()

#plt.yscale('log')
#plt.yscale('linear')
#plt.ylim([1E1, 1E8])