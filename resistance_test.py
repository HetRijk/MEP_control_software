# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 14:50:11 2019

@author: LocalAdmin

Test voltage and current measurement
As the resistance that were measured before were negative
"""


# Standard libraries
import pyvisa as visa
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr

def measurement(tc332, sm2901, meas_time, sample_rate, start_time=time.time()):
    t = instr.time_since(start_time)
    t_meas2 = 0
    t_meas = time.time()
    t_loop = time.time()
    
    temp = list()
    current = list()
    voltage = list()
    setpoints = list()
    while t_meas2 < meas_time:
        # Measuring
        temp.append([t, tc.get_temp(tc332)])
        current.append([t, sm.meas_current(sm2901)]) 
        voltage.append([t, sm.meas_voltage(sm2901)])
        setpoints.append([t, tc.get_setpoint(tc332)])
        
        #Timing
        #Loop
        time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        t_loop = time.time()
        
        # Measurement & Time value
        t_meas2 = instr.time_since(t_meas)
        t = instr.time_since(start_time)
    return temp, current, voltage, setpoints

start_setpoint = 25
sample_rate = 5
meas_time = 10
source_volt = 1E2 
limit_current = 1E-8
sleep_time = 0.5

meas_name = 'wo3189_test_%s_mv_%s_curr' % (source_volt, limit_current)

sample_time = sample_rate**(-1)
meas_len = int(meas_time / sample_time)

tc332 = tc.connect_tc332()
sm2901 = sm.connect_sm2901()

print('Devices connected')

sm.set_voltage(sm2901, source_volt)
sm.set_limit_current(sm2901, limit_current)

tc.set_tuning_mode(tc332, 4)
tc.set_heater_range(tc332, 3)
tc.wait_for_temp(tc332, start_setpoint)
time.sleep(sleep_time)
print('Setup completed')

temp = list()
current = list()
voltage = list()
setpoints = list()

main_time = time.time()

print('Start high measurement at %s' % instr.date_time())
print('And takes %0.2f minutes' % (meas_time/60))

temp1, current1, voltage1, setpoints1 = measurement(tc332, sm2901, meas_time, sample_rate, main_time)

temp += temp1
current += current1
voltage += voltage1
setpoints += setpoints1


temp = np.array(temp).transpose()
current = np.array(current).transpose()
voltage = np.array(voltage).transpose()
setpoints = np.array(setpoints).transpose()

res = np.array([voltage[0], voltage[1]/current[1]])

print('Measurement done')

tc.set_heater_range(tc332, 0)

# Plots
plt.close('all')

try:
    os.mkdir('figures')
except:
    pass

# Voltage
plt.figure(0)
plt.plot(voltage[0], voltage[1])
plt.title('Voltage measured with source voltage %s mV' % source_volt)
plt.xlabel('t(s)')
plt.ylabel('Voltage (V)')

instr.save_plot(r'%s\figures\%s_volt' % (os.getcwd(), meas_name))

# Current
plt.figure(1)
plt.plot(current[0], current[1]*1E9)
plt.title('Current with source voltage %s mV' % source_volt)
plt.xlabel('t(s)')
plt.ylabel('Current (nA)')

instr.save_plot(r'%s\figures\%s_current' % (os.getcwd(), meas_name))

# Resistance
plt.figure(2)
plt.plot(res[0], res[1])
plt.title('Resistance with source voltage %s mV' % source_volt)
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

instr.save_plot(r'%s\figures\%s_resistance' % (os.getcwd(), meas_name))

# Temperature
plt.figure(3)
plt.plot(setpoints[0], setpoints[1])
plt.plot(temp[0], temp[1])
plt.title('Temperatures of heater')
plt.xlabel('t(s)')
plt.ylabel('Temperature (*C)')
plt.legend(['Setpoints', 'Heater'])

instr.save_plot(r'%s\figures\%s_temperature' % (os.getcwd(), meas_name))
