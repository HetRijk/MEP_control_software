# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:08:09 2019

@author: LocalAdmin

Module with functions to control Lakeshore 332 Temperature Controller thorugh a GPIB connection

"""

import visa
import time
import numpy as np
import matplotlib.pyplot as plt

### Constants

kelvin = 273.15

### Setup functions

def connect_tc332(address='GPIB0::12::INSTR'):
    """Sets up connection to the instrument at the address"""
    rm = visa.ResourceManager()
    return rm.open_resource(address)

### Queries
    
def get_device_name(instrument):
    """Queries device name"""
    return instrument.query('*IDN?')

def get_temp(instrument, unit='c'):
    """Queries sensor temperature either in celsius or kelvin"""
    temp = float(instrument.query('KRDG?'))
    if unit == 'c':
        temp = temp + 273.15
    return temp

def get_setpoint(instrument, unit='c'):
    """Queries the setpoint for the heater either in celsius or kelvin. NB make sure the setpoint is set to temperature"""
    setpoint = instrument.query('SETP?')
    if unit == 'c':
        setpoint = setpoint + 273.15
    return setpoint

def get_heater_range(instrument):
    """Query for heater range, 0:off, 1:low, 2:med and 3:high"""
    return instrument.query(range_num)
    
### Control functions
    
def set_heater_range(instrument, range_num):
    """Sets heater range, range_num = 0:off, 1:low, 2:med and 3:high"""
    instrument.write('RANGE ' + str(range_num))
        
    # Check if setting is applied
    times.sleep(0.5)
    range_set = get_heater_range(instrument)
    if range_set != range_num:
        print('Range was NOT set correctly')

def set_setpoint(instrument, setpoint, unit='c'):
    """Set the setpoint for the heater, either in celsius or kelvin. NB make sure the setpoint is set to temperature"""
    instrument.write('SETP ')
        