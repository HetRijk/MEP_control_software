# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:32:44 2019

@author: LocalAdmin

DMM module
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

def meas_voltage(instrument):
    """Measures the voltage of the dmm"""
    volt = instrument.query('MEAS:VOLTage:DC?')
    
    # Source is a string, so values have to be parsed
    value = float(volt[1:7])
    if volt[0] == '-':
        value = -value
    if int(volt[-3:]) != 0:
        value = value*10**int(volt[-3:])
        
    return value

def meas_pressure(instrument):
    """Measures dmm voltage and then converts it into pressure(bars)"""
    volt = meas_voltage(instrument)
    pressure = volt_to_pressure(volt)
    return pressure

def volt_to_pressure(volt):
    """Turns voltage measured into pressure in bars"""
    return volt/10