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

folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\Measurements\WO3193\25 degrees\1112_1542_wo3193_r13_airtoh2\figures'
file_name = '1112_1542_wo3193_r13_airtoh2_resistance'
file = os.path.join(folder, file_name + '.pkl')

#plt.figure()
fig_handle = pkl.load(open(file,'rb'))
fig_handle.show()

#plt.yscale('log')
plt.yscale('linear')
#plt.ylim([1E1, 1E8])