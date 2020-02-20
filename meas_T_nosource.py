# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:54:01 2020

@author: Rijk

Measures the temperature of the Pt1000 and the setpoint of the temperature controller
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

setpoint                = 65
meas_time               = 60*10
sample_rate             = 1

meas_name = 'WO3196_temperature_40C_limit' 


# Preparatory Code
meas_name = str(time.strftime("%m%d_%H%M_")) + meas_name

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

instr.log_and_print(log, "Temperature setpoint is %.2e C" % setpoint)

# =============================================================================
# Connect to devices and setup
# =============================================================================

tc332 = tc.connect_tc332()
instr.log_and_print(log, 'Devices connected')

# =============================================================================
# Measurement
# =============================================================================

instr.log_and_print(log, 'Start measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

temperature = list()
setpoints = list()

main_time = time.time()
t = 0
t_meas = time.time()
t_loop = time.time()
limit_hit = 0

while t < meas_time:
    # Measuring
    t = instr.time_since(main_time)
    temperature.append([t, tc.get_temp(tc332)])
    setpoints.append([t, tc.get_setpoint(tc332)])

    #Timing (If you can  do it better, please do!)
    sleepy_time = sample_rate**-1 - instr.time_since(t_loop)
    if not sleepy_time < 0:
        time.sleep(sleepy_time)
		
    t_loop = time.time()


temperature = np.array(temperature).transpose()
setpoints = np.array(setpoints).transpose()
instr.log_and_print(log, 'Measurement done')

# =============================================================================
# Data processing, plotting and storage
# =============================================================================

# Save measurement data

instr.save_data('%s\%s_temperatures' % (data_folder, meas_name), temperature)
instr.save_data('%s\%s_setpoints' % (data_folder, meas_name), setpoints)

instr.log_mean_std(log, temperature[1], 'temperature')

# Plots
plt.close('all')


# Temperature
plt.figure(3)
plt.plot(setpoints[0], setpoints[1])
plt.plot(temperature[0], temperature[1])
plt.title('Temperatures of heater')
plt.xlabel('t(s)')
plt.ylabel('Temperature (*C)')
plt.legend(['Setpoints', 'Heater'])
plt.grid()

instr.save_plot('%s\%s_temperatures' % (figure_folder, meas_name))

# Close log file
log.close()

