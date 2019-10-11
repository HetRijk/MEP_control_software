# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:59:02 2019

@author: LocalAdmin

Measurement pseudocode

Import libraries

Functions
- code measurement loop with appropriate measurements
    input and output: measurement arrays

Setup
- Connect to instruments
- Set static parameter
- Wait for instruments to reach correct values

Measurement
- start time
- initialise arrays

while loop measurement_time
- measurements 
- append measurements to array
- sleep for sample_time - time_since(time)
- time measurement

Change parameters

Second measurement
- start new loop

End measurement
- Stop output/heater
- disconnect everything

Plotting and saving

"""

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

def measurement(tc332, sm2901, temp, res, setpoints, meas_time, sample_rate, start_time=time.time()):
    t = 0
    t_loop = time.time()
    while t < meas_time:
        temp.append([t, tc.get_temp(tc332)])
        res.append([t, sm.meas_resistance(sm2901)])
        setpoints.append([t, tc.get_setpoint(tc332)])
        time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        t_loop = time.time()
        t = instr.time_since(start_time)
    return temp, res, setpoints

start_setpoint = 35
upper_temp = 100
lower_temp = 35

delta_temp = upper_temp - lower_temp

sample_rate = 5
meas_time = 100

sample_time = sample_rate**(-1)
meas_len = int(meas_time / sample_time)

tc332 = tc.connect_tc332()
sm2901 = sm.connect_sm2901()

print('Devices connected')

tc.set_heater_range(tc332, 3)
tc.wait_for_temp(tc332, start_setpoint)

print('Setup completed')

temp = list()
res = list()
setpoints = list()

print('Start high measurement at %s' % instr.date_time())
start_time = time.time()

set_temps = np.linspace(lower_temp, upper_temp, int(delta_temp/1)+1)
for i in range(len(set_temps)):
    tc.set_setpoint(tc332, set_temps[i])
    temp, res, setpoints = measurement(tc332, sm2901, temp, res, setpoints, 5, sample_rate, start_time)
    
print('Heat up steps down')

for i in range(len(set_temps)):
    tc.set_setpoint(tc332, set_temps[::-1][i])
    temp, res, setpoints = measurement(tc332, sm2901, temp, res, setpoints, 5, sample_rate, start_time)

print('Measurement done')

tc.set_heater_range(tc332, 0)