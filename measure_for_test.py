# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:03:53 2019

@author: LocalAdmin

Measure_for instrument function does not work correctly for get_temp from tc module se here's a test for it
"""

### Import

# Standard libraries
import pyvisa as visa
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr

# Functions to test

def measure_for(instrument, function, meas_time, sample_rate):
    """Measures parameter that the function measures by function for meas_time at sample_rate"""
    #TODO: fix sample rate to take time measurement takes into account
    start_time = time.time()
    t = 0
    meas = list()
    while t < meas_time:
        t = instr.time_since(start_time)
        meas.append([function(instrument), t])
#        print(instr.time_since(t-time.time()))
        #time.sleep(sample_rate**-1 - instr.time_since(t-time.time()) )
        time.sleep(sample_rate**-1)
    meas = np.array(meas)
    return meas

# Code

setpoint = 50
### Miscellaneous functions
start_setpoint = 35
sample_rate = 0.5
meas_time = 100

sample_time = sample_rate**(-1)
meas_len = int(meas_time / sample_time)

# Setup of connections
tc332 = tc.connect_tc332()

# Get heater to starting temperature
print('Wait for start_temp started at %s' % instr.date_time())
tc.set_heater_range(tc332, 2)
#tc.wait_for_temp(tc332, start_setpoint)

tc.set_setpoint(tc332, setpoint)

data = instr.measure_for(tc332, tc.get_temp, meas_time, sample_rate)