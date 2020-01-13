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
import dmm196_module as old_dmm

def measurement(dmm2110, dmm196, meas_time, sample_rate, main_time):
    """Measurement loop"""
    t = instr.time_since(main_time)
    t_meas2 = 0
    t_meas = time.time()
    t_loop = time.time()

    resistance = list()
    pressure = list()
    while t_meas2 < meas_time:
        # Measuring
        pressure.append([t, old_dmm.meas_pressure(dmm196)])
        resistance.append([t, dmm.meas_resistance(dmm2110)])

        #Timing
        if sample_rate**-1 - instr.time_since(t_loop) > 0:
            time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        else:
            pass
        t_loop = time.time()
        t = instr.time_since(main_time)
        t_meas2 = instr.time_since(t_meas)

    return resistance, pressure

sample_rate = 200
meas_time   = 5

meas_name = '33MOhm_dmm_samplerate_test'
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

instr.log_and_print(log, 'Measurement is done with Keithely 2110 DMM')

instr.log_and_print(log, "Sample rate is %s Hz" % sample_rate)
instr.log_and_print(log, "Measurement time is %s s" % meas_time)

# Connect to device
dmm2110 = dmm.connect_dmm2110()
dmm196  = old_dmm.connect_dmm196()

# Set DMM196 to measure DC voltage
old_dmm.mode_dc_voltage(dmm196)

instr.log_and_print(log, 'Devices connected')

resistance  = list()
pressure    = list()

main_time = time.time()

instr.log_and_print(log, 'Start measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

meas_resistance, meas_pressure = measurement(dmm2110, dmm196, meas_time, sample_rate, main_time)

resistance  += meas_resistance
pressure    += meas_pressure

resistance  = np.array(resistance).transpose()
pressure    = np.array(pressure).transpose()

# Save measurement data
instr.save_data('%s\%s_resistance' % (data_folder, meas_name), resistance)
instr.save_data('%s\%s_pressure' % (data_folder, meas_name), pressure)

instr.log_and_print(log, 'Measurement done')

instr.log_mean_std(log, resistance[1], 'resistance')
instr.log_mean_std(log, pressure[1], 'pressure')

# Plots
plt.close('all')

# Resistance
plt.figure(2)
plt.plot(resistance[0], resistance[1])
plt.title('Resistance')
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

instr.save_plot('%s\%s_resistance' % (figure_folder, meas_name))

# Pressure
plt.figure(4)
plt.plot(pressure[0], pressure[1])
plt.title('Pressure in main chamber')
plt.xlabel('t(s)')
plt.ylabel('Pressure (bar)')

instr.save_plot('%s\%s_pressure' % (figure_folder, meas_name))

# Close log file
log.close()
