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
import multimeter_module as dmm

def measurement(sm2901, meas_time, sample_rate, main_time):
    """Measurement loop"""
    t = instr.time_since(main_time)
    t_meas2 = 0
    t_meas = time.time()
    t_loop = time.time()
    limit_hit = 0

    current = list()
    voltage = list()
    while t_meas2 < meas_time:
        # Measuring
        current.append([t, sm.meas_current(sm2901)])
        voltage.append([t, sm.meas_voltage(sm2901)])

        # Check current limit
        limit_current = sm.get_limit_current(sm2901)
        if limit_hit == 1:
            limit_hit = 0
        elif not sm.check_current_limit(sm2901):
            # Discard last measured values
            del current[-1]
            del voltage[-1]
            # Increase limits
            limit_current = sm.get_limit_current(sm2901)
            limit_current = 10*limit_current
            sm.set_limit_current(sm2901, limit_current)
            limit_hit = 1
            instr.log_and_print(log, 'Current limit increased to %0.0e A at %2.1d s after start' % (limit_current, t))

        #Timing
        if sample_rate**-1 - instr.time_since(t_loop) > 0:
            time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        else:
            pass
        t_loop = time.time()
        t = instr.time_since(main_time)
        t_meas2 = instr.time_since(t_meas)

    return current, voltage

sample_rate = 200
meas_time = 60*1
source_volt = 5
limit_current = 1E-4
sleep_time = 0

meas_name = 'sample_rate_test'
meas_name = str(time.strftime("%m%d_%H%M_")) + meas_name


sample_time = sample_rate**(-1)
meas_len = int(meas_time / sample_time)

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

instr.log_and_print(log, meas_name + '\n')

instr.log_and_print(log, 'Measurement is done with voltage sourcing')

instr.log_and_print(log, "Sample rate is %s Hz" % sample_rate)
instr.log_and_print(log, "Measurement time is %s s" % meas_time)
instr.log_and_print(log, "Source voltage is %s V" % source_volt)
instr.log_and_print(log, "Limit current starts at %s A" % limit_current)

# Connect to device
sm2901 = sm.connect_sm2901()
instr.log_and_print(log, 'Devices connected')

sm.set_source_voltage(sm2901, source_volt)
sm.set_limit_current(sm2901, limit_current)


time.sleep(sleep_time)
instr.log_and_print(log, 'Setup completed')

current = list()
voltage = list()
pressure = list()

main_time = time.time()

instr.log_and_print(log, 'Start measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

meas_current, meas_voltage = measurement(sm2901,
										meas_time, sample_rate, main_time)

current += meas_current
voltage += meas_voltage

current = np.array(current).transpose()
voltage = np.array(voltage).transpose()

# Save measurement data

resistances = np.array([voltage[0], voltage[1]/current[1]])

instr.save_data('%s\%s_current' % (data_folder, meas_name), current)
instr.save_data('%s\%s_voltage' % (data_folder, meas_name), voltage)
instr.save_data('%s\%s_resistance' % (data_folder, meas_name), resistances)

instr.log_and_print(log, 'Measurement done')

instr.log_mean_std(log, resistances[1], 'resistance')
instr.log_mean_std(log, voltage[1], 'voltage')
instr.log_mean_std(log, current[1], 'current')

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
plt.plot(resistances[0], resistances[1])
plt.title('Resistance')
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

instr.save_plot('%s\%s_resistance' % (figure_folder, meas_name))

# Close log file
log.close()
