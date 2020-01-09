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

def measurement(dm2110, meas_time, sample_rate, main_time):
    """Measurement loop"""
    t = instr.time_since(main_time)
    t_meas2 = 0
    t_meas = time.time()
    t_loop = time.time()

    resistances = list()
    while t_meas2 < meas_time:
        # Measuring
        resistances.append([t, dmm.meas_resistance(dmm2110)])

        #Timing
        if sample_rate**-1 - instr.time_since(t_loop) > 0:
            time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        else:
            pass
        t_loop = time.time()
        t = instr.time_since(main_time)
        t_meas2 = instr.time_since(t_meas)

    return resistances

sample_rate = 10
meas_time = 60*10
sleep_time = 0

meas_name = '2ndSensor_dmm_test'
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
instr.log_and_print(log, 'Devices connected')

time.sleep(sleep_time)
instr.log_and_print(log, 'Setup completed')

resistances = list()

main_time = time.time()

instr.log_and_print(log, 'Start measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

meas_resistance = measurement(dmm2110, meas_time, sample_rate, main_time)

resistances += meas_resistance

resistances = np.array(resistances).transpose()

# Save measurement data
instr.save_data('%s\%s_resistance' % (data_folder, meas_name), resistances)

instr.log_and_print(log, 'Measurement done')

instr.log_mean_std(log, resistances[1], 'resistance')

# Plots
plt.close('all')

# Resistance
plt.figure(2)
plt.plot(resistances[0], resistances[1])
plt.title('Resistance')
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

instr.save_plot('%s\%s_resistance' % (figure_folder, meas_name))

# Close log file
log.close()
