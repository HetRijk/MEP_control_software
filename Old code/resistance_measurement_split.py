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

def measurement(tc332, sm2901, dmm2100, meas_time, sample_rate, main_time):
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
        pressure.append([t, dmm.meas_pressure(dmm2100)])
        
        # Check current limit
        limit_current = sm.get_limit_current(sm2901)
        if limit_hit == 1:
            limit_hit = 0
        elif not sm.check_limit(sm2901):
            # Discard last measured values
            del temp[-1]
            del current[-1]
            del voltage[-1]
            del setpoints[-1]
            del pressure[-1]

            # Increase limits
            limit_current = sm.get_limit_current(sm2901)
            limit_current = 10*limit_current
            sm.set_limit_current(sm2901, limit_current)
            limit_hit = 1
            instr.log_and_print(log, 'Current limit increased to %0.0e A at %2.1d s after start' % (limit_current, t))
#        elif current[-1][1] < limit_current/100:
#            # Discard last measured values
#            del temp[-1]
#            del current[-1]
#            del voltage[-1]
#            del setpoints[-1]
#            del pressure[-1]
#        
#            # Decrease limits
#            limit_current = limit_current/10
#            sm.set_limit_current(sm2901, limit_current)
#            limit_hit = 1
#            instr.log_and_print(log, 'Current limit decreased to %0.0e A at %2.1d s after start' % (limit_current, t))
        
        #Timing
        time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        t_loop = time.time()
        t = instr.time_since(main_time)
        t_meas2 = instr.time_since(t_meas)
        
    return temp, current, voltage, setpoints, pressure

setpoint = 65
sample_rate = 1
meas_time1 = 60*9
meas_time2 = 60*1
source_volt = 1E3
limit_current = 1E-7
sleep_time = 0

meas_name = 'wo3193_r13_h2_100C' 
meas_name = str(time.strftime("%m%d_%H%M_")) + meas_name

meas_time = meas_time1 + meas_time2

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

instr.log_and_print(log, "Temperature setpoint is %s C" % setpoint)
instr.log_and_print(log, "Sample rate is %s Hz" % sample_rate)
instr.log_and_print(log, "Measurement time is %s s" % meas_time)
instr.log_and_print(log, "Source voltage is %s mV" % source_volt)
instr.log_and_print(log, "Limit current starts at %s A" % limit_current)

# Connect to device
tc332 = tc.connect_tc332()
sm2901 = sm.connect_sm2901()
dmm2100 = dmm.connect_dmm2110()
instr.log_and_print(log, 'Devices connected')

sm.set_source_voltage(sm2901, source_volt)
sm.set_limit_current(sm2901, limit_current)

#tc.set_tuning_mode(tc332, 4)
#tc.set_heater_range(tc332, 3)
#tc.wait_for_temp(tc332, setpoint)
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
                                                                        tc332, sm2901, dmm2100,
                                                                        meas_time1, sample_rate, main_time)

temp += meas_temp
current += meas_current
voltage += meas_voltage
setpoints += meas_setpoints
pressure += meas_pressure

meas_temp, meas_current, meas_voltage, meas_setpoints, meas_pressure = measurement(
                                                                        tc332, sm2901, dmm2100,
                                                                        meas_time2, sample_rate, main_time)

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
plt.title('Voltage measured with source voltage %s mV' % source_volt)
plt.xlabel('t(s)')
plt.ylabel('Voltage (V)')

instr.save_plot('%s\%s_voltage' % (figure_folder, meas_name))

# Current
plt.figure(1)
plt.plot(current[0], current[1]*1E9)
plt.title('Current with source voltage %s mV' % source_volt)
plt.xlabel('t(s)')
plt.ylabel('Current (nA)')

instr.save_plot('%s\%s_current' % (figure_folder, meas_name))

# Resistance
plt.figure(2)
plt.plot(resistances[0], resistances[1])
plt.title('Resistance with source voltage %s mV' % source_volt)
plt.xlabel('t(s)')
plt.ylabel('Resistance (Ohm)')

instr.save_plot('%s\%s_resistance_log' % (figure_folder, meas_name))

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

instr.save_plot('%s\%s_pressure' % (figure_folder, meas_name))

# Close log file
log.close()