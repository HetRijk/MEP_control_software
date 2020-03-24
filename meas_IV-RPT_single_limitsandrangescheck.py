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
from playsound import playsound as play

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr
import multimeter_module as dmm

# =============================================================================
# Settings and prep code
# =============================================================================

source_current_max      = 15E-7
limit_voltage           = 1E1
setpoint                = 65

step_size               = 2*source_current_max/30

sample_time             = 50**-1 * 10
sample_rate             = 0.1
wait_time               = 1

meas_name = 'WO3196dev9_IVcurve_65' 
meas_name = str(time.strftime("%m%d_%H%M_")) + meas_name

# Setting calculations
num_points      = int(2*source_current_max/step_size + 1)

sig_digit = int(-np.floor(np.log10(step_size/10)))
sources = np.linspace(-source_current_max, source_current_max,num_points)           
source_currents    = np.round(np.append(sources, sources[::-1]), sig_digit)

meas_time = len(source_currents)/sample_rate

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
instr.log_and_print(log, "Maximum source current is %s A" % source_current_max)
instr.log_and_print(log, "Limit voltage starts at %s V" % limit_voltage)
instr.log_and_print(log, "Number of points per IV curve is %s" % num_points)
instr.log_and_print(log, "Step size for the IV curves is %.2e A" % step_size)
instr.log_and_print(log, "Temperature setpoint is %.2e C" % setpoint)

# =============================================================================
# Connect to devices and setup
# =============================================================================

tc332 = tc.connect_tc332()
sm2901 = sm.connect_sm2901()
dmm2110 = dmm.connect_dmm2110()
instr.log_and_print(log, 'Devices connected')

sm.set_source_mode_current(sm2901)

# Set sourcemeter to 4-wire measure mode
sm.set_4wire_mode(sm2901)

# Set sourcemeter to turn on on measurement
sm.set_output_on(sm2901)

# Set source current and limit voltage
sm.set_source_current(sm2901, source_currents[0])
sm.set_limit_voltage(sm2901, limit_voltage)

#sm.set_range_current(sm2901, 1e-5)
#sm.set_range_voltage(sm2901, limit_voltage)

# Set sample time
if sample_rate**-1 < sample_time:
    print("Sample rate of %s is too high for the time per sample set of %s" % (sample_rate, sample_time))
    sm.set_meas_time_current(sm2901, np.round(sample_rate**-1, int(-np.floor(np.log10(sample_rate**-1)))))
else:
    sm.set_meas_time_current(sm2901, sample_time)
    
instr.log_and_print(log, 'Setup completed, now waits for %s' % wait_time)

instr.sleep(wait_time)

# =============================================================================
# Measurement
# =============================================================================

main_time = time.time()

instr.log_and_print(log, 'Start measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

main_time = time.time()
t_loop = time.time()


temperature = list()
current = list()
voltage = list()
setpoints = list()
pressure = list()
limits = list()
i_range = list()
v_range = list()

for n, i in enumerate(source_currents):       
    # Measuring
    t = instr.time_since(main_time)
    current.append([t, sm.meas_current(sm2901)])
    voltage.append([t, sm.meas_voltage(sm2901)])
    setpoints.append([t, tc.get_setpoint(tc332)])
    pressure.append([t, dmm.meas_pressure(dmm2110)])
    temperature.append([t, tc.get_temp(tc332)])
    limits.append([t, sm.check_voltage_limit(sm2901)])
    i_range.append([t, sm.get_range_current(sm2901)])
    v_range.append([t, sm.get_range_voltage(sm2901)])
    
    # Set the next source current
    if not n > len(source_currents)-2:
        sm.set_source_current(sm2901, source_currents[n+1])
    
    #Timing
    sleepy_time = sample_rate**-1 - instr.time_since(t_loop)
    if not sleepy_time < 0:
        time.sleep(sleepy_time)
    t_loop = time.time()
    

temperature = np.array(temperature).transpose()
current = np.array(current).transpose()
voltage = np.array(voltage).transpose()
setpoints = np.array(setpoints).transpose()
pressure = np.array(pressure).transpose()
limits = np.array(limits).transpose()
i_range = np.array(i_range).transpose()
v_range = np.array(v_range).transpose() 

# Save measurement data
instr.save_data('%s\%s_current' % (data_folder, meas_name), current)
instr.save_data('%s\%s_voltage' % (data_folder, meas_name), voltage)
instr.save_data('%s\%s_temperatures' % (data_folder, meas_name), temperature)
instr.save_data('%s\%s_setpoints' % (data_folder, meas_name), setpoints)
instr.save_data('%s\%s_pressure' % (data_folder, meas_name), pressure)

instr.save_data('%s\%s_limithit' % (data_folder, meas_name), limits)
instr.save_data('%s\%s_irange' % (data_folder, meas_name), i_range)
instr.save_data('%s\%s_vrange' % (data_folder, meas_name), v_range)

instr.log_and_print(log, 'Measurement done')

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
plt.grid()

instr.save_plot('%s\%s_voltage' % (figure_folder, meas_name))

# Current
plt.figure(1)
plt.plot(current[0], current[1]*1E9)
plt.title('Current')
plt.xlabel('t(s)')
plt.ylabel('Current (nA)')
plt.grid()

instr.save_plot('%s\%s_current' % (figure_folder, meas_name))

# IV Curve
plt.figure(2)
plt.plot(current[1]*1E9, voltage[1])
plt.title('IV Curve')
plt.xlabel('Current (nA)')
plt.ylabel('Voltage (V)')
plt.grid()

instr.save_plot('%s\%s_ivcurve' % (figure_folder, meas_name))

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

# Pressure
plt.figure(4)
plt.plot(pressure[0], pressure[1])
plt.title('Pressure in main chamber')
plt.xlabel('t(s)')
plt.ylabel('Pressure (bar)')
plt.grid()

instr.save_plot('%s\%s_pressure' % (figure_folder, meas_name))

# Limit
plt.figure(5)
plt.plot(limits[0], limits[1])
plt.title('Limit hit during measurement?')
plt.xlabel('t(s)')
plt.ylabel('Limit hit?')
plt.grid()

instr.save_plot('%s\%s_limits' % (figure_folder, meas_name))


# Close log file
log.close()

play('eventually.mp3')