# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 13:05:25 2019

@author: Rijk

Heat up time constant measurement

Heat up from room temperature to 150 degrees with each of the heater ranges
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

# Get heater to startoing temperature
tc.set_heater_range(tc332, start_setpoint)
tc.set_heater_range(tc332, 1)

# Initialise variables
temps_low = np.zeros([2, 1])
temps_med = np.zeros([2, 1])
temps_high = np.zeros([2, 1])

# Get start time and initial temperature
start_time = time.time()
start_temp = tc.get_temp(tc332)
temps_low[0, 0] = start_temp
temps_low[1, 0] = time.time() - start_time

### Start low heater range measurement
# Turn heater on low
#tc.set_heater_range(tc332, 1)

# Start temperature measurement with low heater range
#for t in range(int(meas_len)):
#    temps_low = np.append(temps_low, np.array([tc.get_temp(tc332), time.time() - start_time]))
#    time.sleep(sample_time)
# Wait until heater has cooled down
#tc.set_heater_range(tc332, 0)
#current_temp = tc.get_temp(tc332)
#while current_temp > start_setpoint:
#    current_temp = tc.get_temp(tc332)
#    time.sleep(1)

### Start medium heater range measurement
start_temp = tc.get_temp(tc332)
temps_med[0, 0] = start_temp
temps_med[1, 0] = time.time() - start_time

# Turn heater on medium
tc.set_heater_range(tc332, 2)

# Start temperature measurement with med heater range
for t in range(meas_time):
    temps_med = np.append(temps_med, np.array([tc.get_temp(tc332), time.time() - start_time]))
    time.sleep(sample_time)

# Wait until heater has cooled down
tc.set_heater_range(tc332, 0)
current_temp = tc.get_temp(tc332)
while current_temp > start_setpoint:
    current_temp = tc.get_temp(tc332)
    time.sleep(1)

# Start high heater range measurement
start_temp = tc.get_temp(tc332)
temps_high[0, 0] = start_temp
temps_high[1, 0] = time.time() - start_time

# Turn heater on high
tc.set_heater_range(tc332, 3)

# Start temperature measurement with high heater range
for t in range(meas_time):
    temps_high = np.append(temps_high, np.array([tc.get_temp(tc332), time.time() - start_time]))
    time.sleep(sample_time)
# Turn off the heater
tc.set_heater_range(tc332, 0)
