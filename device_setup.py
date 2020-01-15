# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:09:39 2020

@author: LocalAdmin

Measurement setup setup script
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
import dmm196_module as old_dmm

#dmm2110 = dmm.connect_dmm2110()
#dmm196  = old_dmm.connect_dmm196()
sm2901 = sm.connect_sm2901()
