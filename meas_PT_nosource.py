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

def measurement(tc332, dmm2100, meas_time, sample_rate, main_time):
    """Measurement loop"""
    t = instr.time_since(main_time)
    t_meas2 = 0
    t_meas = time.time()
    t_loop = time.time()
    
    temp = list()
    pressure = list()
    while t_meas2 < meas_time:
        # Measuring
        temp.append([t, tc.get_temp(tc332)])
        pressure.append([t, dmm.meas_pressure(dmm2100)])
        
        #Timing
        time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        t_loop = time.time()
        t = instr.time_since(main_time)
        t_meas2 = instr.time_since(t_meas)
        
    return temp, pressure

sample_rate = 1
meas_time = 60*10
sleep_time = 0

meas_name = 'expansion_temp_test_increaseP_2' 
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

instr.log_and_print(log, "Sample rate is %s Hz" % sample_rate)
instr.log_and_print(log, "Measurement time is %s s" % meas_time)

# Connect to device
tc332 = tc.connect_tc332()
dmm2100 = dmm.connect_dmm2110()
instr.log_and_print(log, 'Devices connected')

#tc.set_tuning_mode(tc332, 4)
#tc.set_heater_range(tc332, 3)
#tc.wait_for_temp(tc332, setpoint)
time.sleep(sleep_time)
instr.log_and_print(log, 'Setup completed')

temp = list()
pressure = list()

main_time = time.time()

instr.log_and_print(log, 'Start measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

meas_temp, meas_pressure = measurement(tc332, dmm2100, meas_time, sample_rate, main_time)

temp += meas_temp
pressure += meas_pressure

temp = np.array(temp).transpose()
pressure = np.array(pressure).transpose()

# Save measurement data
instr.save_data('%s\%s_temperatures' % (data_folder, meas_name), temp)
instr.save_data('%s\%s_pressure' % (data_folder, meas_name), pressure)

instr.log_and_print(log, 'Measurement done')

#tc.set_heater_range(tc332, 0)

# Plots
plt.close('all')

# Temperature
plt.figure(3)
plt.plot(temp[0], temp[1])
plt.title('Temperature of Pt1000')
plt.xlabel('t(s)')
plt.ylabel('Temperature (*C)')

instr.save_plot('%s\%s_temperatures' % (figure_folder, meas_name))

# Pressure
plt.figure(4)
plt.plot(pressure[0], pressure[1])
plt.title('Pressure in main chamber')
plt.xlabel('t(s)')
plt.ylabel('Pressure (bar)')

instr.save_plot('%s\%s_pressure' % (figure_folder, meas_name))

# Close log file
log.close()