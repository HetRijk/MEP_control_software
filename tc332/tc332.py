# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 16:46:47 2019

@author: LocalAdmin

Script to communicate with Lakeshore 332 Temperature Controller

"""

import visa
import time
import numpy as np
import matplotlib.pyplot as plt

def connect(address='GPIB0::12::INSTR'):
    """Sets up connection to the instrument at the address"""
    rm = visa.ResourceManager()
    return rm.open_resource(address)

def get_all_instruments():
    """Gets list of all addresses of connected instrument at the address"""
    rm = visa.ResourceManager()
    return rm.list_resources()

kelvin = 273.15

# Celsius
setpoint = 200
# Hertz
sample_rate = 2 
# Seconds
meas_time = 1000

sample_time = sample_rate**(-1)
meas_len = meas_time / sample_time

tc332 = connect()

idn = tc332.query('*IDN?')
print('Device name is ' + idn)

temp =tc332.query('SETP?')
print('Setpoint is ' + temp)

tc332.write('SETP ' + str(setpoint))
time.sleep(1) 
temp =tc332.query('SETP?')
print('New setpoint is ' + temp) 

now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print('Start rampup at ' + now)

tc332.write('RANGE 3')

temp_rampup = 0
temps = np.zeros([0,0])
while temp_rampup < setpoint + kelvin:
    temp_rampup = float(tc332.query('KRDG?'))
#    temps = temps = np.append(temps, np.array(temp_rampup))
    time.sleep(sample_time)
    
time.sleep(20)

now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print('Start measurement at ' + now)

tc332.write('RANGE 0')

start_time = time.time()
times   = np.zeros([0,0])
for i in range(int(meas_len)):
    temps = np.append(temps, np.array(float(tc332.query('KRDG?')) - kelvin))
    times = np.append(times, time.time() - start_time)
    time.sleep(sample_time)
        
now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print('Measurement done at ' + now)

plt.figure(0)
plt.plot(times, temps)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')