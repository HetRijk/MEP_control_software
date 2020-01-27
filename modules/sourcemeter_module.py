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

# =============================================================================
# Parameters
# =============================================================================

sleepy_time = 0.001

# =============================================================================
# Connection functions
# =============================================================================

def connect_sm2901():
    """Sets up connection to the sourcemeter"""
    address='USB0::0x0957::0x8B18::MY51141059::INSTR'
    rm = visa.ResourceManager()
    return rm.open_resource(address)

# =============================================================================
# Settings functions
# =============================================================================


# Set sourcemeter to a certain mode
def set_4wire_mode(instrument):
    """Sets the sourcemeter to remote mode, thereby enabling 4-wire measurements"""
    instrument.write('SENSE:REMOTE ON')
    
def set_output_on(instrument):
    """Sets instrument to turn output on measurement"""
    instrument.write("OUTPUT:ON:AUTO 1")
    
    
def set_source_mode_current(instrument):
    """Sets instrument to current sourcing"""
    instrument.write('SOURCE:FUNCtion:MODE CURRent')

def set_source_voltage(instrument, volts):
    instrument.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %s' % volts)
    
    # Check if value was set
    time.sleep(sleepy_time)
    volts_actual = get_source_voltage(instrument)
    if volts_actual != volts:
        print('Source voltage was INCORRECTLY set to %s V' % volts)
    else:
        print('Source voltage was set to %s V' % volts)

def set_source_current(instrument, amps):
    instrument.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %s' % amps)
    
    # Check if value was set
    time.sleep(sleepy_time)
    amps_actual = get_source_current(instrument)
    if amps_actual != amps:
        print('Source current was INCORRECTLY set to %s A' % amps)
    else:
        print('Source current was set to %s A' % amps)
    
def set_limit_current(instrument, value):
    """Sets the current limit to value in amperes"""
    instrument.write('SENSe:CURRent:DC:PROTection:LEVel %s' % value)
    
def set_limit_voltage(instrument, value):
    """Sets the voltage limit to value in volts"""
    instrument.write('SENSe:VOLTage:DC:PROTection:LEVel %s' % value)

def set_range_current(instrument, value):
    """Sets the measurement range of the instrument for current"""    
    instrument.write(':SOURce:CURRent:RANGe %G' % value)

    # Check if value was set
    time.sleep(sleepy_time)
    actual_value = get_range_current(instrument)
    if value != actual_value:
        print('Current measurement range was INCORRECTLY set to %s A' % actual_value)
        print('And not to %s A' % value)
    else:
        print('Current measurement range was set to %s A' % actual_value)
    
    
def set_range_voltage(instrument, value):
    """Sets the measurement range of the instrument for voltage"""    
    instrument.write(':SOURce:VOLTage:RANGe %G' % value)
    
    # Check if value was set
    time.sleep(sleepy_time)
    actual_value = get_range_voltage(instrument)
    if value != actual_value:
        print('Voltage measurement range was INCORRECTLY set to %s V' % actual_value)
        print('And not to %s V' % value)
    else:
        print('Voltage measurement range was set to %s V' % actual_value)
    
def set_meas_time_all(instrument, time_meas):
    """Sets measurement time for all measurements"""
    set_meas_time_current(instrument, time_meas)
    set_meas_time_voltage(instrument, time_meas)
    
def set_meas_time_current(instrument, time_meas):
    """Set the measurement time in seconds"""
    instrument.write('SENSE:CURR:DC:APER %s' % time_meas) 
    # Check if value was set
    time.sleep(sleepy_time)
    time_actual = get_meas_time_current(instrument)
    if time_actual != time_meas:
        print('Sample time was INCORRECTLY set to %s s' % time_actual)
        print('And not to %s s' % time_meas)
    else:
        print('Sample time was set to %s s' % time_actual)
            
def set_meas_time_voltage(instrument, time_meas):
    """Set the measurement time in seconds"""
    instrument.write('SENSE:VOLT:DC:APER %s' % time_meas) 
    # Check if value was set
    time.sleep(sleepy_time)
    time_actual = get_meas_time_voltage(instrument)
    if time_actual != time_meas:
        print('Sample time was INCORRECTLY set to %s s' % time_actual)
    else:
        print('Sample time was set to %s s' % time_actual)

# =============================================================================
# Query functions
# =============================================================================

def meas_current(instrument):
    instrument.write(':FORMat:DATA %s' % ('ASCii'))
    return instrument.query_ascii_values(':MEASure:CURRent:DC?')[0]

def meas_voltage(instrument):
    instrument.write(':FORMat:DATA %s' % ('ASCii'))
    return instrument.query_ascii_values(':MEASure:VOLTage:DC?')[0]

def get_source_voltage(instrument):
    """Queries the source voltage of the sourcemeter"""
    return float(instrument.query('SOURce:VOLTage:LEVel:IMMediate:AMPLitude?'))

def get_source_current(instrument):
    """Queries the source current of the sourcemeter"""
    return float(instrument.query('SOURce:CURRent:LEVel:IMMediate:AMPLitude?'))

def get_limit_current(instrument):
    """Queries instrument for current limit set"""
    return float(instrument.query('SENSe:CURRent:DC:PROTection?'))    

def get_limit_voltage(instrument):
    """Queries instrument for voltage limit set"""
    return float(instrument.query('SENSe:VOLTage:DC:PROTection?'))

def get_meas_time_current(instrument):
    """Queries for the measurement time"""
    return float(instrument.query('SENSE:CURR:DC:APER?'))

def get_meas_time_voltage(instrument):
    """Queries for the measurement time"""
    return float(instrument.query('SENSE:VOLT:DC:APER?'))

def get_range_current(instrument):
    """"Queries for the current measurement range"""
    return float(instrument.query('SOURce:CURRent:RANGe?'))

def get_range_voltage(instrument):
    """"Queries for the voltage measurement range"""
    return float(instrument.query('SOURce:VOLTage:RANGe?'))


# =============================================================================
# Compound functions
# =============================================================================

def check_current_limit(instrument):
    """Return Boolean on if current is within limit"""
    return int(instrument.query('SENSe:CURRent:DC:PROTection:TRIPped?'))

def check_voltage_limit(instrument):
    """Return Boolean on if current is within limit"""
    return int(instrument.query('SENSe:VOLTage:DC:PROTection:TRIPped?'))
    