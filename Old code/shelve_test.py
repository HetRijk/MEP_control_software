# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:19:08 2019

@author: LocalAdmin

Shelve save data test
"""

import shelve
import os

T='Hiya'
val=[1,2,3]


folder = '/tmp' 
filename= folder + '/shelve.out'

try:
    os.mkdir(folder)
except:
    pass

my_shelf = shelve.open(filename,'n') # 'n' for new

for key in dir():
    try:
        my_shelf[key] = globals()[key]
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR shelving: {0}'.format(key))
my_shelf.close()

