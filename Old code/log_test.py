# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:15:58 2019

@author: LocalAdmin

Script to test logging
"""

# Standard libraries
import pyvisa as visa
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os

# Custom libraries
import tc332_module as tc
import sourcemeter_module as sm
import instrument_module as instr
import multimeter_module as dmm

# Code

file = 'test' 

start = time.time()

log = open(file + '_log.txt', 'w+')

instr.log_and_print(log, 'Save this message at %s' % instr.time_since(start))

time.sleep(10)

instr.log_and_print(log, 'Here is another one at %s' % instr.time_since(start))

log.close()