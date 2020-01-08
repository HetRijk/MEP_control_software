# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:59:02 2019

@author: LocalAdmin

Measurement pseudocode

Import libraries

Functions
- code measurement loop with appropriate measurements
    input and output: measurement arrays

Setup
- Connect to instruments
- Set static parameter
- Wait for instruments to reach correct values

Measurement
- start time
- initialise arrays

while loop measurement_time
- measurements 
- append measurements to array
- sleep for sample_time - time_since(time)
- time measurement

Change parameters

Second measurement
- start new loop

End measurement
- Stop output/heater
- disconnect everything

Plotting and saving

"""

