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

import visa
import time
import numpy as np
import matplotlib.pyplot as plt

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

def connect_all(addresses):
    instruments = []
    for i in range(len(addresses)):
        try:
            instrument  = connect(addresses[i])
            print('Instrument %s successfully connected' % indentify(addresses[i]))
        except:
            print('Instrument with address %s failed to connect' % addresses[i])
        instruments.append(instrument)
    

def indentify(instrument):
    return instrument.query('*IDN?')
