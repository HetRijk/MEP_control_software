# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 13:05:25 2019

@author: Rijk

Heat up time constant measurement

Heat up from room temperature to 150 degrees with each of the heater ranges
"""

### Import

# Standard libraries
import visa
import time
import numpy as np
import matplotlib.pyplot as plt

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr

### New functions

# Simpler append function

### Input variables

setpoint = 150
sample_rate = 2
meas_time = 1000

### Code

# Setup of connections
tc332 = tc.connect_tc332()

# Set setpoint of tc
tc.set_heater_range(tc332, setpoint)

# Turn on heater
temps_low = np.zeros([0,0])
temps_med = np.zeros([0,0])
temps_high = np.zeros([0,0])

# Get start time and initial temperature
start_time = time.time()
temps_low = 

# Turn heater on low
tc.set_heater_range(tc332, i+1)
    
    # Start temperature measurement
    for t in range(meas_time):
        temps[i,t] = tc.get_temp(tc332)
        
    # Wait until 