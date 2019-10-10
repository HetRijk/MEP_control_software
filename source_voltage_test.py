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

## 1 mV source voltage
#sm.set_voltage(sm2901, 1)
#
#start_time = time.time()
#res_1mv = list()
#for t in range(meas_len):
#    res_1mv.append([instr.time_since(start_time), sm.meas_resistance(sm2901)])
#    time.sleep(sample_time)
#res_1mv = np.array(res_1mv)
#
#mean_1mv = np.mean(res_1mv[1,:])
#std_1mv = np.std(res_1mv[1,:])


source_vs = [0.01, 0.1, 1, 10, 100, 1E3]
res = np.zeros([len(source_vs), meas_len, 2])
for i in range(len(source_vs)):
    sm.set_voltage(sm2901, source_vs[i])

    start_time = time.time()
    for t in range(meas_len):
        res[i, t, :] = [instr.time_since(start_time), sm.meas_resistance(sm2901)]
        time.sleep(sample_time)


# Plotting
#plt.close('close')



#plt.figure(0)
#plt.plot(res_1mv[:,0], res_1mv[:,1])
#plt.title('Resistance for source V of %d mV with mean %d and std %d' % (1, np.mean(res_1mv[:,1]), np.std(res_1mv[:,1])))
#
#plt.figure(1)
#plt.plot(res_10mv[:,0], res_10mv[:,1])
#plt.title('Resistance for source V of %d mV with mean %d and std %d' % (1, np.mean(res_10mv[:,1]), np.std(res_10mv[:,1])))
