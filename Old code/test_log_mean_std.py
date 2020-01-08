# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:34:52 2020

@author: Rijk

Script to test transposing error with log_mean_std function
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

resistance = list()

log = open('test_log', 'w+')

ts = np.linspace(1, 50)
rs = np.random.rand(50)

for i in range(len(ts)):
    resistance.append([ts[i], rs[i]])

resistance = np.array(resistance).transpose()

instr.log_mean_std(log, resistance[1], 'resistance')