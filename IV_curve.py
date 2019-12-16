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

source_volt_start   = -5E3
source_volt_end     = 5E3
num_points_v        = 10

samples_per_v       = 10
sample_rate         = 1

limit_current = 1E-3

meas_name = '33MOhm_resistance_IV_curve_test' 
meas_name = str(time.strftime("%m%d_%H%M_")) + meas_name

# Setting calculations

sample_time     = sample_rate**(-1)
meas_num        = samples_per_v * num_points_v
meas_time_per_v = samples_per_v / sample_rate
meas_time       = meas_num / sample_rate

source_volts    = np.linspace(source_volt_start, source_volt_end, num_points_v)

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
instr.log_and_print(log, "Limit current starts at %s A" % limit_current)

# =============================================================================
# Connect to devices
# =============================================================================

sm2901 = sm.connect_sm2901()
instr.log_and_print(log, 'Devices connected')

sm.set_source_voltage(sm2901, source_volt_start)
sm.set_limit_current(sm2901, limit_current)

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

for i in range(num_points_v):    
    sm.set_source_voltage(sm2901, source_volts[i])
    time.sleep(sample_rate**-1 * 2)
    
    for i in range(samples_per_v):
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

resistances = np.array([voltage[0], voltage[1]/current[1]])

instr.save_data('%s\%s_current' % (data_folder, meas_name), current)
instr.save_data('%s\%s_voltage' % (data_folder, meas_name), voltage)
instr.save_data('%s\%s_resistance' % (data_folder, meas_name), resistances)

instr.log_and_print(log, 'Measurement done')

mean    = np.mean(resistances)
std     = np.std(resistances)
text    = "Mean resistance is %e with std %e" % (mean, std)
instr.log_and_print(log, text)
#tc.set_heater_range(tc332, 0)

# Plots
plt.close('all')

# Voltage
plt.figure(0)
plt.plot(voltage[0], voltage[1])
plt.title('Voltage supplied by Sourcemeter')
plt.xlabel('t(s)')
plt.ylabel('Voltage (V)')

instr.save_plot('%s\%s_voltage' % (figure_folder, meas_name))

# Current
plt.figure(1)
plt.plot(current[0], current[1]*1E9)
plt.title('Current measured by Sourcemeter')
plt.xlabel('t(s)')
plt.ylabel('Current (nA)')

instr.save_plot('%s\%s_current' % (figure_folder, meas_name))

# Resistance
plt.figure(2)
plt.plot(resistances[0], resistances[1])
plt.title('Resistance measured')
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

instr.save_plot('%s\%s_resistance' % (figure_folder, meas_name))

# Resistance
plt.figure(2)
plt.plot(resistances[0], resistances[1])
plt.title('Resistance ')
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

instr.save_plot('%s\%s_resistance_log' % (figure_folder, meas_name))

# Close log file
log.close()