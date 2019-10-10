# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 13:52:54 2019

@author: LocalAdmin

Synchronicity test heater part of the code
"""

### Import

# Standard libraries
import pyvisa as visa
import time
import numpy as np
import matplotlib.pyplot as plt

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr

### Input variables

setpoint = 1
start_setpoint = 45
sample_rate = 10
meas_time = 1000

sample_time = sample_rate**(-1)
meas_len = int(meas_time / sample_time)

### Code
# Setup of connections
tc332 = tc.connect_tc332()

# Get heater to starting temperature
print('Wait for start_temp started at %s' % instr.date_time())
tc.set_heater_range(tc332, 2)
tc.wait_for_temp(tc332, start_setpoint)


start_time = time.time()

tc.set_setpoint(tc332, 45)
tc.set_heater_range(tc332, 3)

time1 = time.time()
data1 = instr.measure_for(tc332, tc.get_temp, 5, sample_rate)

tc.set_setpoint(tc332, 50)

time2 = time.time()
data2 = instr.measure_for(tc332, tc.get_temp, 5, sample_rate)

tc.set_setpoint(tc332, 55)

time3 = time.time()
data3 = instr.measure_for(tc332, tc.get_temp, 5, sample_rate)







