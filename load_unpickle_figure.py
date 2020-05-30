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
import instrument_module as instr

kelvin = 273.15

folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200324 WO3196dev9\Hydrogen\Figures'
file_name = '0324_1758_WO3196dev9_AirToH2_full'
file = os.path.join(folder, file_name + '.pkl')

plt.close('all')

fig_handle = pkl.load(open(file,'rb'))
#fig_handle.show()

#plt.yscale('log')
#plt.yscale('linear')

ax = plt.gca()
lines = ax.lines[0]
ydata1 = lines.get_ydata()
xdata1 = lines.get_xdata()


plt.figure()
plt.plot(xdata1, ydata1, color='k')
#plt.plot(xdata2, (1.38E11*np.exp((-xdata2- min(xdata2))*1.6E-3)+7.06E6)*1E-6 )

plt.legend()
plt.grid()

plt.xlim([min(xdata1), max(xdata1)])
plt.ylim([1.6, 2.8])

plt.xlabel('t (s)')
plt.ylabel('Resistance (M$\Omega$)')