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

sleepy_time = 0.001

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

# =============================================================================
# Setting functions
# =============================================================================

def set_meas_time_all(instrument, time_meas):
    """Set the measurement time for all measurements in seconds or number of PLCs
    (power line cycles: 200 ms for EU grid of 50 Hz)"""
    set_meas_time_current(instrument, time_meas)
    set_meas_time_voltage(instrument, time_meas)
    set_meas_time_resistance(instrument, time_meas)
    
    
def set_meas_time_current(instrument, time_meas):
    """Set the measurement time for current in seconds"""

    instrument.write('SENSE:CURR:DC:APER %s' % time_meas) 
    
    # Check if value was set
    time.sleep(sleepy_time)
    time_actual = get_meas_time_current(instrument)
    if time_actual != time_meas:
        print('Measurement time was NOT correctly set to %s s for current' % time_meas)
    else:
        print('Measurement time was set to %s s for current' % time_meas)
    
    
def set_meas_time_voltage(instrument, time_meas):
    """Set the measurement time for voltage in seconds"""

    instrument.write('SENSE:VOLT:DC:APER %s' % time_meas) 
            
    # Check if value was set
    time.sleep(sleepy_time)
    time_actual = get_meas_time_voltage(instrument)
    if time_actual != time_meas:
            print('Measurement time was NOT correctly set to %s s for voltage' % time_meas)
    else:
            print('Measurement time was set to %s s for voltage' % time_meas)


def set_meas_time_resistance(instrument, time_meas):
    """Set the measurement time for resistance in seconds"""
    instrument.write('SENSE:RESISTANCE:APER %s' % time_meas) 
        
    # Check if value was set
    time.sleep(sleepy_time)
    time_actual = get_meas_time_voltage(instrument)
    if time_actual != time_meas:
        print('Measurement time was NOT correctly set to %s s for resistance' % time_meas)
    else:
        print('Measurement time was set to %s s for resistance' % time_meas)

# =============================================================================
# Query functions
# =============================================================================

def meas_voltage(instrument):
    """Measures the voltage of the dmm"""
    return float(instrument.query('MEAS:VOLTage:DC?'))


def meas_resistance(instrument):
    """Measures the resistance of the dmm"""
    return float(instrument.query('MEAS:RESistance?'))


def meas_pressure(instrument):
    """Measures dmm voltage and then converts it into pressure(bars)"""
    return volt_to_pressure(meas_voltage(instrument))


def volt_to_pressure(volt):
    """Turns voltage measured into pressure in bars"""
    return volt/10


def get_meas_time_current(instrument):
    """Queries for the measurement time"""
    return float(instrument.query('SENSE:CURR:DC:APER?') )


def get_meas_time_voltage(instrument):
    """Queries for the measurement time"""
    return float(instrument.query('SENSE:VOLT:DC:APER?'))


def get_meas_time_resistance(instrument):
    """Queries for the measurement time"""
    return float(instrument.query('SENSE:RESISTANCE:APER?'))
