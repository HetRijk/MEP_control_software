# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 12:49:49 2020

@author: Rijk Hogenbirk

Module with function to uise the Keithley 196 System DMM
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

def connect_dmm196():
    """Sets up connection to the Keithly DMM 196"""
    address = 'GPIB0::7::INSTR'
    rm = visa.ResourceManager()
    return rm.open_resource(address)

def mode_dc_voltage(instrument):
    """Sets dmm to measure dc voltage"""
    instrument.write('F0')
    instrument.write('X')
    
def mode_dc_current(instrument):
    """Sets dmm to measure dc current"""
    instrument.write('F3')
    instrument.write('X')
    
def mode_resistance(instrument):
    """Sets dmm to measure dc voltage"""
    instrument.write('F2')
    instrument.write('X')
    
def get_value(instrument):
    """Queries for the value measured by the DMM
    This DMM does not have specific query commands, 
    so it will just return what is curerntly set to measure"""
    
    return instrument.query('')

def convert_to_volt(data):
    """Converts DMM196 format to floating volt value"""
    value = float(data[6:13])
    if data[5] == '-':
        value = -value
    exp_sign = 1
    if int(data[15]) != 0:
        if data[14] == '-':
            exp_sign = -1        
        value = value*10**(exp_sign * int(data[-3:]))
        
    return value

def meas_voltage(instrument):
    """Queries DMM and converts output string to voltage value"""
    data = get_value(instrument)
    voltage = convert_to_volt(data)
    return voltage

def meas_pressure(instrument):
    """Measures dmm voltage and then converts it into pressure(bars)"""
    volt = meas_voltage(instrument)
    pressure = volt_to_pressure(volt)
    return pressure

def volt_to_pressure(volt):
    """Turns voltage measured into pressure in bars"""
    return volt/10