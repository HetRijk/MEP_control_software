# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:34:28 2019

@author: Rijk Hogenbirk

Script to measure the IV curve with the Sourcemeter as a voltage source and current measurement device
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
import multimeter_module as dmm

# =============================================================================
# Settings
# =============================================================================

source_current_start    = -1E-7
source_current_end      = 1E-7
limit_voltage           = 1E1


num_points_i            = 11

samples_per_i       = 10
sample_rate         = 1


meas_name = '33MOhm_resistance_IV_curve_test' 
meas_name = str(time.strftime("%m%d_%H%M_")) + meas_name

# Setting calculations

sample_time     = sample_rate**(-1)
meas_num        = samples_per_i * num_points_i
meas_time_per_i = samples_per_i / sample_rate
meas_time       = meas_num / sample_rate

source_currents    = np.linspace(source_current_start, source_current_end, num_points_i)

# Setup folder structure and initialise log
data_folder = meas_name + '\data'
figure_folder = meas_name + '\\figures'

try:
    os.mkdir(meas_name)
    try:
        os.mkdir(data_folder)
    except:
        pass
    try:
        os.mkdir(figure_folder)
    except:
        pass
except:
    pass

log = open(meas_name + '\\' + meas_name + '_log.txt', 'w+')

instr.log_and_print(log, "Sample rate is %s Hz" % sample_rate)
instr.log_and_print(log, "Measurement time is %s s" % meas_time)
instr.log_and_print(log, "Limit voltage starts at %s V" % limit_voltage)

# =============================================================================
# Connect to devices
# =============================================================================

sm2901 = sm.connect_sm2901()
instr.log_and_print(log, 'Devices connected')

sm.set_source_current(sm2901, source_current_start)
sm.set_limit_voltage(sm2901, limit_voltage)

#Set measurement time
sm.set_meas_time_voltage(sm2901, 10, unit='plc')

# Check that sample rate is not faster than the measurement time


instr.log_and_print(log, 'Setup completed')

# =============================================================================
# Measurement
# =============================================================================

main_time = time.time()

instr.log_and_print(log, 'Start measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

t = instr.time_since(main_time)
t_loop = time.time()
limit_hit = 0

current = list()
voltage = list()

for i in range(num_points_i):    
    sm.set_source_current(sm2901, source_currents[i])
    time.sleep(sample_rate**-1 * 2)
    
    for i in range(samples_per_i):
        # Measuring
        current.append([t, sm.meas_current(sm2901)])
        voltage.append([t, sm.meas_voltage(sm2901)])
        
        #Timing
        sleepy_time =sample_rate**-1 - instr.time_since(t_loop)
        if not sleepy_time < 0:
            time.sleep(sleepy_time)
        t_loop = time.time()
        t = instr.time_since(main_time)

current = np.array(current).transpose()
voltage = np.array(voltage).transpose()

# Save measurement data

resistance = np.array([voltage[0], voltage[1]/current[1]])

instr.save_data('%s\%s_current' % (data_folder, meas_name), current)
instr.save_data('%s\%s_voltage' % (data_folder, meas_name), voltage)
instr.save_data('%s\%s_resistance' % (data_folder, meas_name), resistance)

instr.log_and_print(log, 'Measurement done')

mean    = np.mean(resistance)
std     = np.std(resistance)
text    = "Mean resistance is %e with std %e" % (mean, std)
instr.log_and_print(log, text)
#tc.set_heater_range(tc332, 0)

# Plots
plt.close('all')

# Voltage
plt.figure(0)
plt.plot(voltage[0], voltage[1])
plt.title('Voltage')
plt.xlabel('t(s)')
plt.ylabel('Voltage (V)')

instr.save_plot('%s\%s_voltage' % (figure_folder, meas_name))

# Current
plt.figure(1)
plt.plot(current[0], current[1]*1E9)
plt.title('Current')
plt.xlabel('t(s)')
plt.ylabel('Current (nA)')

instr.save_plot('%s\%s_current' % (figure_folder, meas_name))

# Resistance
plt.figure(2)
plt.plot(resistance[0], resistance[1])
plt.title('Resistance measured')
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

instr.save_plot('%s\%s_resistance' % (figure_folder, meas_name))

# Resistance
plt.figure(3)
plt.plot(resistance[0], resistance[1])
plt.title('Resistance ')
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

plt.yscale('log')

instr.save_plot('%s\%s_resistance_log' % (figure_folder, meas_name))

# Close log file
log.close()