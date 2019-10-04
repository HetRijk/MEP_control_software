# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 14:25:57 2019

@author: LocalAdmin

Test for appending a vector to a matrix with acquired measurement data
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


### Variables

sample_rate = 5
meas_time = 200

sample_time = sample_rate**(-1)
meas_len = int(meas_time / sample_time)

## Code
sm2901 = sm.connect_sm2901()

sm.set_voltage(sm2901, 1)

print('Start measurement, takes until %s' % instr.time_later(meas_time))

start_time = time.time()
R = np.zeros([2,1])
current_array = np.zeros([2,1])
for i in range(meas_len):
    current_array[0] = sm.meas_resistance(sm2901)
    current_array[1] = time.time() - start_time
    R = np.concatenate((R, current_array), axis=1)
    time.sleep(sample_time)

R = np.delete(R, 0,1)
