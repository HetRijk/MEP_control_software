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
    
#def set_current(instrument, amps):
#    instrument.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %s' % amps)

def set_source_voltage(instrument, volts):
    instrument.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %s' % volts)
    
    # Check if value was set
    time.sleep(0.5)
    volts_actual = get_source_voltage(instrument)
    if volts_actual != volts:
        print('Source voltage was NOT correctly set to %s V' % volts)
    else:
        print('Source voltage was set to %s V' % volts)

def set_source_current(instrument, amps):
    instrument.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %s' % amps)
    
    # Check if value was set
    time.sleep(0.5)
    amps_actual = get_source_current(instrument)
    if amps_actual != amps:
        print('Source current was NOT correctly set to %s A' % amps)
    else:
        print('Source current was set to %s A' % amps)
    
def set_limit_current(instrument, value):
    """Sets the current limit to value in amperes"""
    instrument.write('SENSe:CURRent:DC:PROTection:LEVel %s' % value)
    
def set_limit_voltage(instrument, value):
    """Sets the voltage limit to value in volts"""
    instrument.write('SENSe:VOLTage:DC:PROTection:LEVel %s' % value)    
    
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

def meas_plusminus_current(instrument, source_max, num_points):
    """Measures current as source voltage is varied between -source_max and source_max.
    Should include 0, so num_points has to uneven number and at least 3."""
    if num_points < 3 and num_points % 2 != 1:
        print('Num_points should be at least 3 and uneven')
    else:
        sources = np.linspace(-source_max, source_max, num_points)
        currents = list()
        for i in range(len(sources)):
            set_source_voltage(instrument, sources[i])
            time.sleep(0.01)
            currents.append(meas_current(instrument))
    return currents, sources

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

def get_source_current(instrument):
    """Queries the source current of the sourcemeter"""
    source = instrument.query('SOURce:CURRent:LEVel:IMMediate:AMPLitude?')
    
    # Source is a string, so values have to be parsed
    value = float(source[1:7])
    if source[0] == '-':
        value = -value
    if int(source[12:16]) != 0:
        value = value*10**int(source[12:16])
        
    return value

def get_limit_current(instrument):
    """Queries instrument for current limit set"""
    limit = instrument.query('SENSe:CURRent:DC:PROTection?')
    
    # Source is a string, so values have to be parsed
    value = float(limit[1:7])
    if limit[0] == '-':
        value = -value
    if int(limit[12:16]) != 0:
        value = value*10**int(limit[12:16])
    
    return value
    
def get_limit_voltage(instrument):
    """Queries instrument for voltage limit set"""
    limit = instrument.query('SENSe:VOLTage:DC:PROTection?')
    
    # Source is a string, so values have to be parsed
    value = float(limit[1:7])
    if limit[0] == '-':
        value = -value
    if int(limit[12:16]) != 0:
        value = value*10**int(limit[12:16])
    
    return value

def check_current_limit(instrument):
    """Return Boolean on if current is within limit"""
    value = instrument.query('SENSe:CURRent:DC:PROTection:TRIPped?')[0]
    if value == '0':
        return_value = True
    else:
        return_value = False
    return return_value


def check_voltage_limit(instrument):
    """Return Boolean on if current is within limit"""
    value = instrument.query('SENSe:VOLTage:DC:PROTection:TRIPped?')[0]
    if value == '0':
        return_value = True
    else:
        return_value = False
    return return_value