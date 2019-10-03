# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:31:13 2019

@author: LocalAdmin
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


### New functions

# Simpler append function

# Cooldown function
def cooldown(instrument, setpoint):
    """Shuts off heater and waits until its has cooled down"""
    tc.set_heater_range(instrument, 0)
    current_temp = tc.get_temp(instrument)
    while current_temp > setpoint:
        current_temp = tc.get_temp(instrument)
        time.wait(1)


### Input variables

setpoint = 150
start_setpoint = 25
sample_rate = 2
meas_time = 1000

sample_time = sample_rate**(-1)
meas_len = meas_time / sample_time

### Code
# Setup of connections
tc332 = tc.connect_tc332()

# Get heater to starting temperature
tc.set_setpoint(tc332, start_setpoint)