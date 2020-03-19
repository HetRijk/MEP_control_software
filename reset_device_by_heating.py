# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:09:39 2020

@author: LocalAdmin

Heats device to reset it for the next hydrogen measurement
Slowly heat it to 100C and leave it there for 10 minutes, then let it cooldown
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

dmm2110 = dmm.connect_dmm2110()
dmm196  = old_dmm.connect_dmm196()
sm2901 = sm.connect_sm2901()
tc332 = tc.connect_tc332()

start_temp = 50
max_temp = 65
step_temp = 2
step_time = 5
wait_time = 1

print('Device temp starts at %.2e C' % start_temp)

temps = np.round(np.linspace(start_temp, max_temp, int((max_temp-start_temp)/step_temp) + 1))

print('Start measurement at %s' % instr.date_time())
print('And will take %s s' % (len(temps)*step_time + wait_time))

tc.set_heater_range(tc332, 3)
for i, t in enumerate(temps):
    tc.set_setpoint(tc332, t)
    time.sleep(step_time)
    
print('Heatup to %.2e C done' % max_temp)
print('Now waits for %s s' % wait_time)

time.sleep(wait_time)

print('Waiting done')
#print('Reset to start temperature')

#tc.set_setpoint(tc332, start_temp)
