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

kelvin = 273.15

folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\Measurements\WO3189\Time constants 25C\1024_1258_wo3189_r13\figures'
file_name = '1024_1258_wo3189_r13_pressure'
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

lines = ax.lines[1]
ydata2 = lines.get_ydata()
xdata2 = lines.get_xdata()

print('Fit starts at %g' % xdata2[0])
print('Fit ends at %g' % xdata2[-1])

plt.figure()
plt.plot(xdata1 - kelvin, ydata1*1E-6, label='Measured')
plt.plot(xdata2 - kelvin, ydata2*1E-6, label='Arrhenius Fit')
#plt.plot(xdata2, (1.38E11*np.exp((-xdata2- min(xdata2))*1.6E-3)+7.06E6)*1E-6 )

plt.legend()
plt.grid()

#plt.xlim([1300, 2000])
#plt.ylim([0, 30])

plt.xlabel('T ($^\circ$C)')
plt.ylabel('Resistance (M$\Omega$)')