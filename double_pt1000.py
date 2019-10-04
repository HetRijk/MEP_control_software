# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:41:51 2019

@author: LocalAdmin

Script to run test for comparing the two Pt1000's with each other mounted on the same heater
"""

### Import

# Standard libraries
import pyvisa as visa
import time
import datetime as dtime
import numpy as np
import matplotlib.pyplot as plt

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr

### Variables

sample_rate = 5
meas_time = 1000

sample_time = sample_rate**(-1)
meas_len = int(meas_time / sample_time)

### Code
sm2901 = sm.connect_sm2901()

sm.set_voltage(sm2901, 1)

R = np.zeros([meas_len,2])
V = np.zeros([meas_len,1])
I = np.zeros([meas_len,1])
T = np.zeros([meas_len,1])
start_time = time.time()
for i in range(meas_len):    
    R[i,0] = sm.meas_resistance(sm2901)
    R[i,1] = time.time() - start_time
    print('Measurement %s out of %s' % (i+1, meas_len))
    time.sleep(sample_time)
    
R_test = V/I   
