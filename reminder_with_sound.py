# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:06:43 2020

@author: RijkHogenbirk

PLays sounds after a set amount of time to make sure I do stuff for the measurement
"""

# Standard libraries
import pyvisa as visa
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os

# Specific libs
import instrument_module as instr
from playsound import playsound as play

time1 = 60*5

time2 = 60*10

ahead = 10

start = time.time()

while instr.time_since(start) < time1 - ahead:
      instr.sleep(5)
      
print('Set main and air chamber to vacuum')
play('eventually.mp3')


while instr.time_since(start) < time2 - ahead:
      instr.sleep(5)

print('Set main chamber to ambient pressure (10V)')
play('eventually.mp3')

