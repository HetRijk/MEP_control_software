# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:32:44 2019

@author: LocalAdmin

DMM module for the Keithley 2110 5 1/2 Digit Multimeter
"""

# Standard libraries
import pyvisa as visa
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import os

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr
import multimeter_module as dmm

def connect_dmm2100():
    """Sets up connection to the Keithly DMM 2100"""
    address = 'USB0::0x05E6::0x2100::1416380::INSTR'
    rm = visa.ResourceManager()
    return rm.open_resource(address)

def connect_dmm2110():
    """Sets up connection to the Keithly DMM 2110, not the 2100"""
    address = 'USB0::0x05E6::0x2110::8010814::INSTR'
    rm = visa.ResourceManager()
    return rm.open_resource(address)

def set_meas_time_all(instrument, time_meas, unit='plc'):
    """Set the measurement time for all measurements in seconds or number of PLCs
    (power line cycles: 200 ms for EU grid of 50 Hz)"""
    set_meas_time_current(instrument, time_meas, unit='plc')
    set_meas_time_voltage(instrument, time_meas, unit='plc')
    set_meas_time_resistance(instrument, time_meas, unit='plc')
    
    
def set_meas_time_current(instrument, time_meas, unit='plc'):
    """Set the measurement time for current in seconds or number of PLCs
    (power line cycles: 200 ms for EU grid of 50 Hz)"""
    if unit == 'plc':
        instrument.write('SENSE:CURR:DC:NPLC %s' % time_meas)
    elif unit == 's':
        instrument.write('SENSE:CURR:DC:APER %s' % time_meas) 
    else:
        print('Unit of measurement time_meas not given correctly for current')
            
    # Check if value was set
    time.sleep(0.5)
    time_actual = get_meas_time_current(instrument, unit)
    if time_actual != time_meas:
        if unit == 'plc':
            print('Measurement time was NOT correctly set to %s PLC for current' % time_meas)
        elif unit == 's':
            print('Measurement time was NOT correctly set to %s s for current' % time_meas)
    else:
        if unit == 'plc':
            print('Measurement time was set to %s PLC for current' % time_meas)
        elif unit == 's':
            print('Measurement time was set to %s s for current' % time_meas)
    
def set_meas_time_voltage(instrument, time_meas, unit='plc'):
    """Set the measurement time for voltage in seconds or number of PLCs
    (power line cycles: 200 ms for EU grid of 50 Hz)"""
    if unit == 'plc':
        instrument.write('SENSE:VOLT:DC:NPLC %s' % time_meas)
    elif unit == 's':
        instrument.write('SENSE:VOLT:DC:APER %s' % time_meas) 
    else:
        print('Unit of measurement time_meas not given correctly for voltage')
            
    # Check if value was set
    time.sleep(0.5)
    time_actual = get_meas_time_voltage(instrument, unit)
    if time_actual != time_meas:
        if unit == 'plc':
            print('Measurement time was NOT correctly set to %s PLC for voltage' % time_meas)
        elif unit == 's':
            print('Measurement time was NOT correctly set to %s s for voltage' % time_meas)
    else:
        if unit == 'plc':
            print('Measurement time was set to %s PLC for voltage' % time_meas)
        elif unit == 's':
            print('Measurement time was set to %s s for voltage' % time_meas)

def set_meas_time_resistance(instrument, time_meas, unit='plc'):
    """Set the measurement time for resistance in seconds or number of PLCs
    (power line cycles: 200 ms for EU grid of 50 Hz)"""
    if unit == 'plc':
        instrument.write('SENSE:RESISTANCE:NPLC %s' % time_meas)
    elif unit == 's':
        instrument.write('SENSE:RESISTANCE:APER %s' % time_meas) 
    else:
        print('Unit of measurement time_meas not given correctly for resistance')
            
    # Check if value was set
    time.sleep(0.5)
    time_actual = get_meas_time_voltage(instrument, unit)
    if time_actual != time_meas:
        if unit == 'plc':
            print('Measurement time was NOT correctly set to %s PLC for resistance' % time_meas)
        elif unit == 's':
            print('Measurement time was NOT correctly set to %s s for resistance' % time_meas)
    else:
        if unit == 'plc':
            print('Measurement time was set to %s PLC for resistance' % time_meas)
        elif unit == 's':
            print('Measurement time was set to %s s for resistance' % time_meas)

def meas_voltage(instrument):
    """Measures the voltage of the dmm"""
    volt = instrument.query('MEAS:VOLTage:DC?')
    
    # Source is a string, so values have to be parsed
    value = float(volt[1:7])
    if volt[0] == '-':
        value = -value
    exp_sign = 1
    if int(volt[-3:]) != 0:
        if volt[-4] == '-':
            exp_sign = -1        
        value = value*10**(exp_sign * int(volt[-3:]))
        
    return value

def meas_resistance(instrument):
    """Measures the resistance of the dmm"""
    resistance = instrument.query('MEAS:RESistance?')
    
    # Source is a string, so values have to be parsed
    value = float(resistance[1:11])
    if resistance[0] == '-':
        value = -value
    exp_sign = 1
    if int(resistance[-3:-1]) != 0:
        if resistance[-4] == '-':
            exp_sign = -1        
        value = value*10**(exp_sign * int(resistance[-3:]))
        
    return value

def meas_pressure(instrument):
    """Measures dmm voltage and then converts it into pressure(bars)"""
    volt = meas_voltage(instrument)
    pressure = volt_to_pressure(volt)
    return pressure

def volt_to_pressure(volt):
    """Turns voltage measured into pressure in bars"""
    return volt/10

def get_meas_time_current(instrument, unit='plc'):
    """Queries for the measurement time"""
    if unit=='plc':
        sample_time = instrument.query('SENSE:CURR:DC:NPLC?')
    elif unit=='s':
        sample_time = instrument.query('SENSE:CURR:DC:APER?') 
    else:
        print('Unit of measurement time not given correctly for query')
        sample_time = '+1.00000000E+000\n'
    
    # Source is a string, so values have to be parsed
    value = float(sample_time[1:7])
    if sample_time[0] == '-':
        value = -value
    if int(sample_time[12:16]) != 0:
        value = value*10**int(sample_time[12:16])
        
    return value

def get_meas_time_voltage(instrument, unit='plc'):
    """Queries for the measurement time"""
    if unit=='plc':
        sample_time = instrument.query('SENSE:VOLT:DC:NPLC?')
    elif unit=='s':
        sample_time = instrument.query('SENSE:VOLT:DC:APER?') 
    else:
        print('Unit of measurement time not given correctly for query')
        sample_time = '+1.00000000E+000\n'
    
    # Source is a string, so values have to be parsed
    value = float(sample_time[1:7])
    if sample_time[0] == '-':
        value = -value
    if int(sample_time[12:16]) != 0:
        value = value*10**int(sample_time[12:16])
        
    return value

def get_meas_time_resistance(instrument, unit='plc'):
    """Queries for the measurement time"""
    if unit=='plc':
        sample_time = instrument.query('SENSE:RESISTANCE:NPLC?')
    elif unit=='s':
        sample_time = instrument.query('SENSE:RESISTANCE:APER?') 
    else:
        print('Unit of measurement time not given correctly for query')
        sample_time = '+1.00000000E+000\n'
    
    # Source is a string, so values have to be parsed
    value = float(sample_time[1:7])
    if sample_time[0] == '-':
        value = -value
    if int(sample_time[12:16]) != 0:
        value = value*10**int(sample_time[12:16])
        
    return value