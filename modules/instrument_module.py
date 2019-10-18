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
import pickle as pkl
import os

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
    """Measures parameter that the function measures by function for meas_time at sample_rate.
    NB Use np.array to turn list into numpy array after measurement is done."""
    start_time = time.time()
    t = 0
    t_loop = time.time()
    meas = list()
    while t < meas_time:
        meas.append([t, function(instrument)])
        
        time.sleep(sample_rate**-1 - instr.time_since(t_loop))
        print(instr.time_since(t_loop))
        t_loop = time.time()
        t = instr.time_since(start_time)
    return meas
  

# Timing functions

def date_time():
    return datetime.datetime.now()

def time_since(start_time):
    """Returns time since start_time"""
    return time.time() - start_time

def time_later(extra_time):
    """Gives the time 'extra_time' seconds past now"""
    extra_time = int(extra_time / 60)
    now = datetime.datetime.now()
    text = now + datetime.timedelta(minutes = extra_time)
    return text

# Saving functions
    
def save_plot(file_name):
    """Saves current plot, both as pickle (figure) and .svg (image)"""
    plt.savefig(file_name + '.svg')
    plt.savefig(file_name + '.PNG')
    
    fig     = plt.gcf()

    with open(file_name + '.pkl', 'wb') as fid:
        pkl.dump(fig, fid)

    print('Plot saved as \n%s' % file_name)
    
def save_data(file_name, data):
    """Saves data as file_name.csv"""
    np.savetxt(file_name+'.csv', data, delimiter=',')
    


### Miscellaneous functions
    
def pt1000_temp(resistance):
    temperature = 1E-05*resistance**2 + 0.2311*resistance - 243.32
    return temperature

def pt1000_res(temperature):
    resistance = -6E-4*temperature**2 + 3.9197*temperature + 998.96
    return resistance

