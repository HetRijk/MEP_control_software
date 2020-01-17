"""
Edits by Rijk @20200115
    - Removed 
        - commented code
        - unused libraries
        - overwritten changes in working directory
    - Made sure np.linespace() num parameters given are integers
    - Changed visa instrument ask method to query as ask is outdated
    - Changed raw_input to input as raw_input does not exist in Python3 and input functions the same
    - Removed waitingTime parameter as it is useless
"""

import os
import time
import numpy as np
import visa
import scipy.io as sio
import matplotlib.pyplot as plt
import ATSM #custom module

os.chdir('D:\Martin\HTSC_alpha') 

# Instrument setup (for both channels)
Keysight = visa.instrument('USB0::2391::36376::MY51143303::0::INSTR')

Keysight.write(':SOUR1:FUNC:MODE CURR')
Keysight.write(":SENS1:REM ON")#for 4 wire connection
Keysight.write(":OUTP1 OFF")
Keysight.write(":SENS1:WAIT ON")
Keysight.write(":SENS1:WAIT:AUTO ON")

Keysight.write(':SOUR2:FUNC:MODE CURR')
Keysight.write(":SENS2:REM ON")#for 4 wire connection
Keysight.write(":OUTP2 OFF")
Keysight.write(":SENS2:WAIT ON")
Keysight.write(":SENS2:WAIT:AUTO ON")

# Temperature range and resolution parameters
rampRate    = 20
targetT     = 200
stepT       = 2

temperature = list([])
temperature.extend(np.arange(4.5,targetT,stepT))
temperature.extend(np.arange(5,temperature[-1],stepT)[::-1])


def getDC():
    #aux = keithley.query(':MEAS:VOLT?')
    return 1#float(aux.split(',')[0])


print('Input filename:   '),
name = input()
fileName = str(name)

if (os.path.isfile(fileName)):
    raise IOError("File already exists")
  
initI1      = 0
targetI1    = 10e-6
stepI1      = 1000e-9

initI2      = 0
targetI2    = 100e-6
stepI2      = 1000e-9

Keysight.write(":SENS1:VOLT:PROT 1")
Keysight.write(":SENS2:VOLT:PROT 1")

Keysight.write(":OUTP1 ON")
Keysight.write(":OUTP2 ON")

for i,t in enumerate(temperature):
    ATSM.ramp(1,t,rampRate)
    
    while abs(round(ATSM.getT(),2) - t) > 0.1: # requirement to have the tcurrent T at least above (x-1).85, where x is the set T
        time.sleep(2)
    time.sleep(1);
    print('Current T: %f.' %ATSM.getT());
    
    DCiSource1=[]
    DCiSource1.extend(np.linspace(initI1, targetI1, int((targetI1-initI1)/stepI1+1)))
    DCiSource1.extend(np.linspace(targetI1,-targetI1,  int(2*(targetI1)/stepI1+1)))   
    DCiSource1.extend(np.linspace(-targetI1, initI1, int((targetI1-initI1)/stepI1+1)))
    
    voltages1=[]
    currents1=[]
    
    DCiSource2=[]
    DCiSource2.extend(np.linspace(initI2, targetI2, int((targetI2-initI2)/stepI2+1)))
    DCiSource2.extend(np.linspace(targetI2,-targetI2,  int(2*(targetI2)/stepI2+1)))   
    DCiSource2.extend(np.linspace(-targetI2, initI2, int((targetI2-initI2)/stepI2+1)))
    
    voltages2=[]
    currents2=[]
    
    for k,I in enumerate(DCiSource1):
        print('New set I1: %f.' %DCiSource1[k])
    
        Keysight.write(':sour1:curr %.9f' %I)
        
        time.sleep(0.01)
        DCCurrent1=float(Keysight.query(':meas:curr? (@1)'))
        DCVoltage1=float(Keysight.query(':meas:volt? (@1)'))
        startTime = time.time()

        print('Doin da measurement...')

        voltages1.extend([DCVoltage1])
        currents1.extend([DCCurrent1])
        
        plt.figure(1)
        plt.plot(voltages1,currents1)
        plt.xlabel('V (V)')
        plt.ylabel('I (A)')
        plt.draw()    
        plt.pause(0.001)

    for k,I in enumerate(DCiSource2):
        print('New set I2: %f.' %DCiSource2[k])
    
        Keysight.write(':sour2:curr %.9f' %I)
        
        time.sleep(0.01)
        DCCurrent2=float(Keysight.query(':meas:curr? (@2)'))
        DCVoltage2=float(Keysight.query(':meas:volt? (@2)'))
        startTime = time.time()

        print('Doin da measurement...')

        voltages2.extend([DCVoltage2])
        currents2.extend([DCCurrent2])
        
        plt.figure(2)
        plt.plot(voltages2,currents2)
        plt.xlabel('V (V)')
        plt.ylabel('I (A)')
        plt.draw()    
        plt.pause(0.001)
        

        
    plt.figure(1)    
    plt.clf()
    plt.plot(currents1,voltages1)
    plt.title(fileName)
    plt.ylabel('V (V)')
    plt.xlabel('I (A)')
    plt.savefig(fileName +str('_ch1_%.2fK' %t) + '.png')
    
    plt.figure(2)    
    plt.clf()
    plt.plot(currents2,voltages2)
    plt.title(fileName)
    plt.ylabel('V (V)')
    plt.xlabel('I (A)')
    plt.savefig(fileName +str('_ch2_%.2fK'%t) + '.png')
    
    sio.savemat(fileName+str('_ch1_%.2fK'%t)+'_'+str(targetI1/1e-6)+'uA_max',{'voltages':np.array(voltages1),'currents':np.array(currents1),'temp':ATSM.getT()})
    sio.savemat(fileName+str('_ch2_%.2fK'%t)+'_'+str(targetI2/1e-6)+'uA_max',{'voltages':np.array(voltages2),'currents':np.array(currents2),'temp':ATSM.getT()})
            
    print('Ya measurement is saved!')

Keysight.write(":OUTP1 OFF")
Keysight.write(":OUTP2 OFF")

print('Measurement done.')