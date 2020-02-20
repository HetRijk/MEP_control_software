# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:09:39 2020

@author: LocalAdmin

Measurement setup setup script
"""


# Standard libraries
import pyvisa as visa
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr
import multimeter_module as dmm
import dmm196_module as old_dmm

tc332 = tc.connect_tc332()
dmm2110 = dmm.connect_dmm2110()
dmm196  = old_dmm.connect_dmm196()
sm2901 = sm.connect_sm2901()

temperature = list()
current = list()
voltage = list()
setpoints = list()
pressure = list()
t = list()

#dmm.set_meas_time_all(dmm2110, 0.02)
#dmm2110.write('SENSE:VOLTAGE:RESOLUTION MAX')
#print(dmm2110.query('SENSE:VOLTAGE:RESOLUTION?'))

main_time = time.time()

sm.meas_current(sm2901)
sm.meas_voltage(sm2901)
tc.get_setpoint(tc332)
tc.get_temp(tc332)
dmm.meas_pressure(dmm2110)
#dmm2110.query('MEAS:VOLT:DC? 10,0.003')

print(instr.time_since(main_time))
print(dmm2110.query('SENSE:VOLTAGE:RESOLUTION?'))