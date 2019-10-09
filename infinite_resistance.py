# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 16:57:42 2019

@author: LocalAdmin

Script for measuring the resistance with the sourcemeter until code is manually stopped
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

### Variables

sample_rate = 5
meas_time = 10

sample_time = sample_rate**(-1)
meas_len = int(meas_time / sample_time)

### Code
sm2901 = sm.connect_sm2901()

sm.set_voltage(sm2901, 1)

start_time = time.time()
res_1mv = list()
for t in range(meas_len):
    res_1mv.append([sm.meas_resistance(sm2901), instr.time_since(start_time)])
    time.sleep(sample_time)
res_1mv = np.array(res_1mv)

sm.set_voltage(sm2901, 10)

start_time = time.time()
res_10mv = list()
for t in range(meas_len):
    res_10mv.append([sm.meas_resistance(sm2901), instr.time_since(start_time)])
    time.sleep(sample_time)
res_10mv = np.array(res_10mv)

