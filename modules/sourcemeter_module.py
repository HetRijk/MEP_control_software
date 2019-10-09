# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 17:51:32 2019

@author: LocalAdmin

Control code for the Keysight B2901A Sourcemeter

Conventions:
SM: Sourcemeter

"""

import pyvisa as visa
import time
import numpy as np
import matplotlib.pyplot as plt

## Setup functions

def connect_sm2901():
    """Sets up connection to the sourcemeter"""
    address='USB0::0x0957::0x8B18::MY51141059::INSTR'
    rm = visa.ResourceManager()
    return rm.open_resource(address)

## Settings functions
    
def set_current(instrument, amps):
    instrument.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %s' % amps)

def set_voltage(instrument, mvolts):
    volts = mvolts * 10**-3
    instrument.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %s' % volts)
    
    # Check if value was set
    time.sleep(0.5)
    volts_actual = get_source_voltage(instrument)
    if volts_actual != volts:
        print('Source voltage was NOT correctly set to %s mV' % mvolts)
    else:
        print('Source voltage was set to %s mV' % mvolts)
    

## Query functions

def meas_current(instrument):
    instrument.write(':FORMat:DATA %s' % ('ASCii'))
    return instrument.query_ascii_values(':MEASure:CURRent:DC?')[0]

def meas_voltage(instrument):
    instrument.write(':FORMat:DATA %s' % ('ASCii'))
    return instrument.query_ascii_values(':MEASure:VOLTage:DC?')[0]

def meas_resistance(instrument):
    instrument.write(':FORMat:DATA %s' % ('ASCii'))
    V = instrument.query_ascii_values(':MEASure:VOLTage:DC?')[0]
    I = instrument.query_ascii_values(':MEASure:CURRent:DC?')[0]
    return V/I

def get_source_voltage(instrument):
    """Queries the source voltage of the sourcemeter"""
    source = instrument.query('SOURce:VOLTage:LEVel:IMMediate:AMPLitude?')
    
    # Source is a string, so values have to be parsed
    value = float(source[1:7])
    if source[0] == '-':
        value = -value
    if int(source[12:16]) != 0:
        value = value*10**int(source[12:16])
        
    return value