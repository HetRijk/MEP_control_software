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

def arrhenius(T, A, Ea):
    kb = 8.617333262145E-5 #eV/K
    return A * np.exp( Ea / (kb*T))

folder = r'C:\Users\Rijk\Documents\MEP\MEP_control_software\20200305 WO3196dev1\20200316 WO3196dev1 R_T'
file_name = '0316_1457_WO3196dev1_Tsteps5C_RvsT_fit'
file = os.path.join(folder, file_name + '.pkl')

# =============================================================================
# Open old figure and plot new one
# =============================================================================

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

plt.close('all')

#xdata3 = np.linspace(xdata2[0] - 10, )

plt.figure()
#plt.plot(xdata1 - kelvin, ydata1*1E-6, label='Measured')
plt.plot(xdata2 - kelvin, ydata2*1E-6, label='Fit')
plt.plot(xdata2 - kelvin, (arrhenius(xdata2, 125.278, 0.405485)*1E-6 + 0.01), label='Check')

plt.legend()
plt.grid()

#plt.xlim([20, 105])
#plt.ylim([0, int(1E3)])
#
plt.xlabel(u'Temperature (\u00B0C)')
plt.ylabel('Resistance (M$\Omega$)')

#instr.save_plot(os.path.join(folder, file_name) + '_fig')