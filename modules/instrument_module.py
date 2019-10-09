# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 17:54:03 2019

General VISA instrument control module

@author: Rijk Hogenbirk

General comments:
    - import as ctrl:
        import instrument_control as ctrl

Open questions/todos:
    - How to build on this module to create other modules?
        import into more specific modules for each kind of or specific instrument
"""

# Standard libraries
import pyvisa as visa
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr

## Setup functions

def connect(address):
    """Sets up connection to the instrument at the address"""
    try:
        rm = visa.ResourceManager()
    except:
        print('Instrument on %s not connected' % address)
    return rm.open_resource(address)


def get_all_instruments():
    """Gets list of all addresses of connected instrument at the address"""
    rm = visa.ResourceManager()
    addresses = rm.list_resources()
    return addresses

# Does not connect to any instruments
#def connect_all(addresses):
#    instruments = []
#    for i in range(len(addresses)):
#        try:
#            instrument  = connect(addresses[i])
#            print('Instrument %s successfully connected' % indentify(addresses[i]))
#        except:
#            print('Instrument with address %s failed to connect' % addresses[i])
#        instruments.append(instrument)
#    return instruments

def indentify(instrument):
    return instrument.query('*IDN?')

# Measurement functions

def measure_for(instrument, function, meas_time, sample_rate):
    """Measures parameter that the function measures by function for meas_time at sample_rate"""
    #TODO: fix sample rate to take time measurement takes into account
    start_time = time.time()
    t = 0
    meas = list()
    while t < meas_time:
        t = instr.time_since(start_time)
        meas.append([function(instrument), t])
        print(instr.time_since(t-time.time()))
        #time.sleep(sample_rate**-1 - instr.time_since(t-time.time()) )
        time.sleep(sample_rate**-1)
    meas = np.array(meas)
    return meas

### Miscellaneous functions

def date_time():
    return datetime.datetime.now()

def time_since(start_time):
    return time.time() - start_time

def time_later(extra_time):
    """Gives the time 'extra_time' seconds past now"""
    extra_time = int(extra_time / 60)
    now = datetime.datetime.now()
    text = now + datetime.timedelta(minutes = extra_time)
    return text
