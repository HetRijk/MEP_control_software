# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 12:39:01 2020

@author: LocalAdmin
"""

res_frac = 3e-4

meas_range = float(dmm2110.query('SENSE:VOLT:RANGE?'))

#dmm2110.write('SENSE:VOLTAGE:RESOLUTION %s' % (meas_range*res_frac))
dmm2110.write('SENSE:VOLTAGE:RESOLUTION MAX')

print('DMM Resolution is %s ' %dmm2110.query('SENSE:VOLTAGE:RESOLUTION?'))