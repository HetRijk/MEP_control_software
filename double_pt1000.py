# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:41:51 2019

@author: LocalAdmin

Script to run test for comparing the two Pt1000's with each other mounted on the same heater
"""

### Import

# Standard libraries
import pyvisa as visa
import time
import numpy as np
import matplotlib.pyplot as plt

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr

### Code

rm = visa.ResourceManager()

all_instruments = rm.list_resources()

instr.connect_all(all_instruments)


sm2901 = sm.connect_sm2901()

print(sm.meas_resistance)