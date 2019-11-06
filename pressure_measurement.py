# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 18:45:29 2019

@author: LocalAdmin

Measuring pressure
"""

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

def measurement(dmm2100, meas_time, sample_rate, main_time):
    """Measurement loop"""
    t = instr.time_since(main_time)
    t_meas2 = 0
    t_meas = time.time()
    t_loop = time.time()
    
    voltage = list()
    pressure = list()
    while t_meas2 < meas_time:
        # Measuring
        pressure.append([t, dmm.meas_pressure(dmm2100)])
        voltage.append([t, dmm.meas_voltage(dmm2100)])
        
        #Timing
        time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        t_loop = time.time()
        t = instr.time_since(main_time)
        t_meas2 = instr.time_since(t_meas)
        
    return voltage, pressure

setpoint = 65
sample_rate = 1
meas_time = 60
source_volt = 1E2
limit_current = 1E-6
sleep_time = 0

meas_name = 'mixing_pressure_test_small_main_continuation' 
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

# Connect to device
dmm2100 = dmm.connect_dmm2110()
instr.log_and_print(log, 'Devices connected')


#tc.set_tuning_mode(tc332, 4)
#tc.set_heater_range(tc332, 3)
#tc.wait_for_temp(tc332, setpoint)
time.sleep(sleep_time)
instr.log_and_print(log, 'Setup completed')

pressure = list()
voltage = list()

main_time = time.time()

instr.log_and_print(log, 'Start high measurement at %s' % instr.date_time())
instr.log_and_print(log, 'And takes %0.2f minutes' % (meas_time/60))

meas_voltage, meas_pressure = measurement(dmm2100, meas_time, sample_rate, main_time)
pressure    += meas_pressure
voltage     += meas_voltage
pressure    = np.array(pressure).transpose()
voltage     = np.array(voltage).transpose()

instr.save_data('%s\%s_pressure' % (data_folder, meas_name), pressure)

instr.log_and_print(log, 'Measurement done')
#tc.set_heater_range(tc332, 0)

# Plots
plt.close('all')

# Pressure
plt.figure(4)
plt.plot(pressure[0], pressure[1])
plt.title('Pressure in main chamber')
plt.xlabel('t(s)')
plt.ylabel('Pressure (bar)')

instr.save_plot('%s\%s_pressure' % (figure_folder, meas_name))

# Close log file
log.close()

