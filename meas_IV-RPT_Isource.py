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
# Settings and prep code
# =============================================================================

source_current_max      = 1E-7
limit_voltage           = 1E1

step_size               = source_current_max / 10

sample_time             = 10#provide in # of PLC
samples_per_step        = 10
sample_rate             = 1

meas_name = '33MOhm_resistance_IV_curve_test' 
meas_name = str(time.strftime("%m%d_%H%M_")) + meas_name

# Setting calculations
num_points      = int(2*source_current_max/step_size + 1)
meas_num        = samples_per_step * num_points
sample_time     = samples_per_step / sample_rate
meas_time       = meas_num / sample_rate

source_currents    = np.linspace(-source_current_max, source_current_max, num_points)

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
# Connect to devices and setup
# =============================================================================

sm2901 = sm.connect_sm2901()
instr.log_and_print(log, 'Devices connected')

sm.set_source_current(sm2901, source_currents[0])
sm.set_limit_voltage(sm2901, limit_voltage)

# Set sample time
sample_time = 50**-1*sample_time
if sample_rate**-1 < sample_time:
    print("Sample rate of %s is too high for the time per sample set of %s" % (sample_rate, sample_time))
    sample_time = sample_rate**-1/50**-1
    dmm.set_meas_time_resistance(sm2901, sample_time)
else:
    dmm.set_meas_time_resistance(sm2901, )
    
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

for i in range(num_points):    
    sm.set_source_current(sm2901, source_currents[i])
    time.sleep(sample_rate**-1 * 2)
    
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

# =============================================================================
# Data processing, plotting and storage
# =============================================================================

# Save measurement data
instr.save_data('%s\%s_current' % (data_folder, meas_name), current)
instr.save_data('%s\%s_voltage' % (data_folder, meas_name), voltage)

instr.log_and_print(log, 'Measurement done')

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

# Close log file
log.close()