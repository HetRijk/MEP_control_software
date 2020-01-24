# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 14:50:11 2019

@author: Rijk Hogenbirk

Script to measure the ohmic resistance, pressure and temperature 
with the Keysight B2901A Sourcemeter as a current source and voltage measurement device
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
# Input Parameters
# =============================================================================

source_current  = 1E-7
limit_voltage   = 1E1
meas_time       = 60*10
setpoint        = 25

sample_time     = 50**-1 * 10
sample_rate     = 4

wait_time       = 10

meas_name = 'WO3196_ohmic_air_light'

# =============================================================================
# Preperatory code
# =============================================================================

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

instr.log_and_print(log, 'Measurement is done with current sourcing')

instr.log_and_print(log, "Sample rate is %s Hz" % sample_rate)
instr.log_and_print(log, "Sample time has been set to %s s" % sample_time)
instr.log_and_print(log, "Measurement time is %s s" % meas_time)
instr.log_and_print(log, "Source current is %s A" % source_current)
instr.log_and_print(log, "Limit voltage starts at %s V" % limit_voltage)
instr.log_and_print(log, "Temperature setpoint is %.2e C" % setpoint)

# =============================================================================
# Connect to devices and setup
# =============================================================================

tc332 = tc.connect_tc332()
sm2901 = sm.connect_sm2901()
dmm2110 = dmm.connect_dmm2110()
instr.log_and_print(log, 'Devices connected')

# Set sourcemeter to 4-wire measure mode
sm.set_4wire_mode(sm2901)

# Set sourcemeter to turn on on measurement
sm.set_output_on(sm2901)

# Set source current and limit voltage
sm.set_source_current(sm2901, source_current)
sm.set_limit_voltage(sm2901, limit_voltage)

# Set sample time
if sample_rate**-1 < sample_time:
    print("Sample rate of %s is too high for the time per sample set of %s" % (sample_rate, sample_time))
    sm.set_meas_time_current(sm2901, np.round(sample_rate**-1, int(-np.floor(np.log10(sample_rate**-1)))))
else:
    sm.set_meas_time_current(sm2901, sample_time)
    
instr.log_and_print(log, 'Setup completed, now waits for %s s' % wait_time)

time.sleep(wait_time)

# =============================================================================
# Measurement
# =============================================================================

instr.log_and_print(log, 'Start measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

temperature = list()
current = list()
voltage = list()
setpoints = list()
pressure = list()

main_time = time.time()
t = 0
t_meas = time.time()
t_loop = time.time()
limit_hit = 0

while t < meas_time:
    # Measuring
    t = instr.time_since(main_time)
    current.append([t, sm.meas_current(sm2901)])
    voltage.append([t, sm.meas_voltage(sm2901)])
    temperature.append([t, tc.get_temp(tc332)])
    setpoints.append([t, tc.get_setpoint(tc332)])
    pressure.append([t, dmm.meas_pressure(dmm2110)])

    # Check current limit
    limit_voltage = sm.get_limit_voltage(sm2901)
    if limit_hit == 1:
        limit_hit = 0
    elif sm.check_voltage_limit(sm2901):
        # Increase limits
        limit_voltage = sm.get_limit_voltage(sm2901)
        limit_voltage = 10*limit_voltage
        sm.set_limit_voltage(sm2901, limit_voltage)
        limit_hit = 1
        instr.log_and_print(log, 'Voltage limit increased to %0.0e V at %2.1d s after start' % (limit_voltage, t))

    #Timing (If you can  do it better, please do!)
    sleepy_time = sample_rate**-1 - instr.time_since(t_loop)
    if not sleepy_time < 0:
        time.sleep(sleepy_time)
		
    t_loop = time.time()


temperature = np.array(temperature).transpose()
current = np.array(current).transpose()
voltage = np.array(voltage).transpose()
setpoints = np.array(setpoints).transpose()
pressure = np.array(pressure).transpose()

instr.log_and_print(log, 'Measurement done')

# =============================================================================
# Data processing, plotting and storage
# =============================================================================

# Save measurement data

resistances = np.array([voltage[0], voltage[1]/current[1]])

instr.save_data('%s\%s_current' % (data_folder, meas_name), current)
instr.save_data('%s\%s_voltage' % (data_folder, meas_name), voltage)
instr.save_data('%s\%s_resistance' % (data_folder, meas_name), resistances)
instr.save_data('%s\%s_temperatures' % (data_folder, meas_name), temperature)
instr.save_data('%s\%s_setpoints' % (data_folder, meas_name), setpoints)
instr.save_data('%s\%s_pressure' % (data_folder, meas_name), pressure)

instr.log_mean_std(log, resistances[1], 'resistance')
instr.log_mean_std(log, voltage[1], 'voltage')
instr.log_mean_std(log, current[1], 'current')
instr.log_mean_std(log, pressure[1], 'pressure')
instr.log_mean_std(log, temperature[1], 'temperature')

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

# Temperature
plt.figure(3)
plt.plot(setpoints[0], setpoints[1])
plt.plot(temperature[0], temperature[1])
plt.title('Temperatures of heater')
plt.xlabel('t(s)')
plt.ylabel('Temperature (*C)')
plt.legend(['Setpoints', 'Heater'])

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
