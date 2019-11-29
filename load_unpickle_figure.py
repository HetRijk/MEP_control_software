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

folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\Measurements\WO3189\Important ones\Time constants 65C\1031_1552_wo3189_r13_h2toair\figures'
file_name = '1031_1552_wo3189_r13_h2toair_resistance'
file = os.path.join(folder, file_name + '.pkl')

plt.figure(0)
fig_handle = pkl.load(open(file,'rb'))
fig_handle.show()

plt.yscale('log')
#plt.ylim([1E1, 1E8])