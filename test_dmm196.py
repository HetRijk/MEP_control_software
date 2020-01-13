# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 13:32:26 2020

@author: LocalAdmin
"""

import dmm196_module as dmm2

dmm196 = dmm2.connect_dmm196()

print(dmm2.meas_voltage(dmm196))