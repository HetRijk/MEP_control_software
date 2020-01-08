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

def measurement(tc332, sm2901, dmm2110, meas_time, sample_rate, main_time):
    """Measurement loop"""
    t = instr.time_since(main_time)
    t_meas2 = 0
    t_meas = time.time()
    t_loop = time.time()
    limit_hit = 0
    
    temp = list()
    current = list()
    voltage = list()
    setpoints = list()
    pressure = list()
    while t_meas2 < meas_time:
        # Measuring
        temp.append([t, tc.get_temp(tc332)])
        current.append([t, sm.meas_current(sm2901)])
        voltage.append([t, sm.meas_voltage(sm2901)])
        setpoints.append([t, tc.get_setpoint(tc332)])
        pressure.append([t, dmm.meas_pressure(dmm2110)])
        
        # Check current limit
        limit_voltage = sm.get_limit_voltage(sm2901)
        if limit_hit == 1:
            limit_hit = 0
        elif not sm.check_voltage_limit(sm2901):
            # Discard last measured values
            del temp[-1]
            del current[-1]
            del voltage[-1]
            del setpoints[-1]
            del pressure[-1]

            # Increase limits
            limit_voltage = sm.get_limit_voltage(sm2901)
            limit_voltage = 10*limit_voltage
            sm.set_limit_voltage(sm2901, limit_voltage)
            limit_hit = 1
            instr.log_and_print(log, 'Voltage limit increased to %0.0e V at %2.1d s after start' % (limit_voltage, t))

        #Timing
        if sample_rate**-1 - instr.time_since(t_loop) > 0:
            time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        else:
            pass
        t_loop = time.time()
        t = instr.time_since(main_time)
        t_meas2 = instr.time_since(t_meas)
        
    return temp, current, voltage, setpoints, pressure

setpoint = 65
sample_rate = 5
meas_time = 60*5
source_current = 1E-8
limit_voltage = 1E0
sleep_time = 0

meas_name = '33MOhm_outside' 
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

instr.log_and_print(log, 'Measurement is done with current sourcing')

instr.log_and_print(log, "Sample rate is %s Hz" % sample_rate)
instr.log_and_print(log, "Measurement time is %s s" % meas_time)
instr.log_and_print(log, "Source current is %s A" % source_current)
instr.log_and_print(log, "Limit voltage starts at %s V" % limit_voltage)
instr.log_and_print(log, "Temperature setpoint is %s C" % setpoint)
# Connect to device
tc332 = tc.connect_tc332()
sm2901 = sm.connect_sm2901()
dmm2110 = dmm.connect_dmm2110()
instr.log_and_print(log, 'Devices connected')

sm.set_source_current(sm2901, source_current)
sm.set_limit_voltage(sm2901, limit_voltage)
time.sleep(sleep_time)
instr.log_and_print(log, 'Setup completed')

temp = list()
current = list()
voltage = list()
setpoints = list()
pressure = list()

main_time = time.time()

instr.log_and_print(log, 'Start measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

meas_temp, meas_current, meas_voltage, meas_setpoints, meas_pressure = measurement(
                                                                        tc332, sm2901, dmm2110,
                                                                        meas_time, sample_rate, main_time)

temp += meas_temp
current += meas_current
voltage += meas_voltage
setpoints += meas_setpoints
pressure += meas_pressure


temp = np.array(temp).transpose()
current = np.array(current).transpose()
voltage = np.array(voltage).transpose()
setpoints = np.array(setpoints).transpose()
pressure = np.array(pressure).transpose()

# Save measurement data

resistances = np.array([voltage[0], voltage[1]/current[1]])

instr.save_data('%s\%s_temperatures' % (data_folder, meas_name), temp)
instr.save_data('%s\%s_current' % (data_folder, meas_name), current)
instr.save_data('%s\%s_voltage' % (data_folder, meas_name), voltage)
instr.save_data('%s\%s_setpoints' % (data_folder, meas_name), setpoints)
instr.save_data('%s\%s_resistance' % (data_folder, meas_name), resistances)
instr.save_data('%s\%s_pressure' % (data_folder, meas_name), pressure)

instr.log_and_print(log, 'Measurement done')

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
plt.plot(temp[0], temp[1])
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

#plt.ylim([0, max(pressure[1])])

instr.save_plot('%s\%s_pressure' % (figure_folder, meas_name))

# Close log file
log.close()