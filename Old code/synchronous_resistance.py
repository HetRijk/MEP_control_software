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
meas_time = 60

source_volt = 100

sample_time = sample_rate**(-1)
meas_len = int(meas_time / sample_time)

### Code
sm2901 = sm.connect_sm2901()

sm.set_voltage(sm2901, 100)

start_time = time.time()
data_res = instr.measure_for(sm2901, sm.meas_resistance, meas_time, sample_rate)
