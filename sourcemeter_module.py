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

def connect_sm2901(address='GPIB0::12::INSTR'):
    """Sets up connection to the instrument at the address"""
    rm = visa.ResourceManager()
    return rm.open_resource(address)

## Settings functions
    
def set_current(amps, instrument):
    instrument.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %s' % amps)

def set_voltage(volts, instrument):
    instrument.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %s' % volts)

## Measurement functions

def meas_current(instrument):
    instrument.write(':FORMat:DATA %s' % ('ASCii'))
    return instrument.query_ascii_values(':MEASure:CURRent:DC?')[0]

def meas_voltage(instrument):
    instrument.write(':FORMat:DATA %s' % ('ASCii'))
    return instrument.query_ascii_values(':MEASure:VOLTage:DC?')[0]

def meas_resistance(instrument):
    volt = meas_voltage(instrument)
    current = meas_current(instrument)
    return volt/current

