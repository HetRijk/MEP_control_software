"""
Martin Lee - TNW

Tue, 14 Jan, 16:30 (3 days ago)

to me

The command for 2wire-4wire is
Keysight.write(":SENS1:REM ON")
I think. Double check.

Cheers,
-Martin
"""


import os
os.chdir('D:\Dejan')
#import medVNA
#import Montana
import time
import numpy as np
from scipy import signal
from numpy import *
import visa
#import Montana
import scipy.io as sio
#import Rigol
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
#import keithley2701 as keith
#import keithley2000 as keith2000
import ATSM

ATSM.setup()
ATSM.defineZones([20,20,20])
os.chdir('D:\Makars\Valencia')

os.chdir('D:\Martin\HTSC_alpha')
#import optimizePosition

#global Rig
#Rig = visa.instrument('USB0::0x1AB1::0x0E11::DP8B171900446::INSTR')
#Keysight = visa.instrument('USB0::2391::35608::MY51141059::0::INSTR') #old
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




rampRate=20
targetT = 200
stepT=2
temperature = list([])
temperature.extend(np.arange(4.5,targetT,stepT))
temperature.extend(np.arange(5,temperature[-1],stepT)[::-1])


def getDC():
    #aux = keithley.ask(':MEAS:VOLT?')
    return 1#float(aux.split(',')[0])


print('Input filename:   '),
name = raw_input()
fileName = str(name)

if (os.path.isfile(fileName)):
    raise IOError("File already exists")

waitingTime = 10

initI1=0
targetI1=10e-6
stepI1=1000e-9

initI2=0
targetI2=100e-6
stepI2=1000e-9

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

    DCiSource1.extend(np.linspace(initI1, targetI1, (targetI1-initI1)/stepI1+1))
    DCiSource1.extend(np.linspace(targetI1,-targetI1,  2*(targetI1)/stepI1+1))
    DCiSource1.extend(np.linspace(-targetI1, initI1, (targetI1-initI1)/stepI1+1))


    voltages1=[]
    currents1=[]


    DCiSource2=[]

    DCiSource2.extend(np.linspace(initI2, targetI2, (targetI2-initI2)/stepI2+1))
    DCiSource2.extend(np.linspace(targetI2,-targetI2,  2*(targetI2)/stepI2+1))
    DCiSource2.extend(np.linspace(-targetI2, initI2, (targetI2-initI2)/stepI2+1))


    voltages2=[]
    currents2=[]




    for k,I in enumerate(DCiSource1):
        print('New set I1: %f.' %DCiSource1[k])

        #flakeVoltageCollect = list([])
        #flakeVoltage=0
        #ATSM.ramp(1,t, rampRate)
       # while abs(round(ATSM.getT(),1) - t) > 0.05: # requirement to have the tcurrent T at least above (x-1).85, where x is the set T
       #     time.sleep(2)
        #time.sleep(5)
       # print('Current T: %f.' %ATSM.getT())
    #    for k in range(50):
    #        flakeVoltageCollect.append(keith2000.getDC())
    #        pause(0.0001)
    #    for l in range(50):
    #        flakeVoltage=flakeVoltage+(flakeVoltageCollect[l])
    #    flakeVoltage=flakeVoltage/50

        Keysight.write(':sour1:curr %.9f' %I)
        #if V<9:
    #        Rig.write(':SOUR%d:volt %.3f' %(1,V))
    #    else:
    #        Rig.write(':SOUR%d:volt %.3f' %(2,V-8))
        time.sleep(0.01)
        DCCurrent1=float(Keysight.ask(':meas:curr? (@1)'))
        DCVoltage1=float(Keysight.ask(':meas:volt? (@1)'))
        startTime = time.time()
       # freq = np.linspace(Xstart,Xstop,Xpoints)
        #fileName = fileName + str('%02.d'%counter) + '.mat'
       # traces = zeros(Xpoints)+0j
        print('Doin da measurement...')
        #traces = medVNA.doMeasurement('S21',averages)
       # pdVoltage = keith2000.getDC()
        #DCValue=keith2000.getDC()
        voltages1.extend([DCVoltage1])
        currents1.extend([DCCurrent1])


        plt.figure(1)
        plot(voltages1,currents1)
        plt.xlabel('V (V)')
        plt.ylabel('I (A)')
        plt.draw()
        plt.pause(0.001)



       # print('New set T: %f.' %temperature[i+1])
        #print('New set T: %f.' %DCPullVoltage[i+1])
        #counter += 1

    for k,I in enumerate(DCiSource2):
        print('New set I2: %f.' %DCiSource2[k])

        #flakeVoltageCollect = list([])
        #flakeVoltage=0
        #ATSM.ramp(1,t, rampRate)
       # while abs(round(ATSM.getT(),1) - t) > 0.05: # requirement to have the tcurrent T at least above (x-1).85, where x is the set T
       #     time.sleep(2)
        #time.sleep(5)
       # print('Current T: %f.' %ATSM.getT())
    #    for k in range(50):
    #        flakeVoltageCollect.append(keith2000.getDC())
    #        pause(0.0001)
    #    for l in range(50):
    #        flakeVoltage=flakeVoltage+(flakeVoltageCollect[l])
    #    flakeVoltage=flakeVoltage/50

        Keysight.write(':sour2:curr %.9f' %I)
        #if V<9:
    #        Rig.write(':SOUR%d:volt %.3f' %(1,V))
    #    else:
    #        Rig.write(':SOUR%d:volt %.3f' %(2,V-8))
        time.sleep(0.01)
        DCCurrent2=float(Keysight.ask(':meas:curr? (@2)'))
        DCVoltage2=float(Keysight.ask(':meas:volt? (@2)'))
        startTime = time.time()
       # freq = np.linspace(Xstart,Xstop,Xpoints)
        #fileName = fileName + str('%02.d'%counter) + '.mat'
       # traces = zeros(Xpoints)+0j
        print('Doin da measurement...')
        #traces = medVNA.doMeasurement('S21',averages)
       # pdVoltage = keith2000.getDC()
        #DCValue=keith2000.getDC()

        voltages2.extend([DCVoltage2])
        currents2.extend([DCCurrent2])



        plt.figure(2)
        plot(voltages2,currents2)
        plt.xlabel('V (V)')
        plt.ylabel('I (A)')
        plt.draw()
        plt.pause(0.001)



    plt.figure(1)
    plt.clf()
    plot(currents1,voltages1)
    plt.title(fileName)
    plt.ylabel('V (V)')
    plt.xlabel('I (A)')
    savefig(fileName +str('_ch1_%.2fK'%t) + '.png')
    plt.figure(2)
    plt.clf()
    plot(currents2,voltages2)
    plt.title(fileName)
    plt.ylabel('V (V)')
    plt.xlabel('I (A)')
    savefig(fileName +str('_ch2_%.2fK'%t) + '.png')
    #
    #print('New set T: %f.' %temperature[i+1])
    sio.savemat(fileName+str('_ch1_%.2fK'%t)+'_'+str(targetI1/1e-6)+'uA_max',{'voltages':np.array(voltages1),'currents':np.array(currents1),'temp':ATSM.getT()})
    sio.savemat(fileName+str('_ch2_%.2fK'%t)+'_'+str(targetI2/1e-6)+'uA_max',{'voltages':np.array(voltages2),'currents':np.array(currents2),'temp':ATSM.getT()})
    #    sio.savemat(fileName + str('_%03.d'%counter)+str('_%.1fK'%t),{'temp':ATSM.getT(),'flakeVoltage':flakeVoltage})

    print('Ya measurement is saved!')
#keith2000.close()
#Rig.write(':SOUR%d:volt %.3f' %(3,2))
#medVNA.power(power)
#medVNA.send(':INITiate:CONTinuous:ALL ON')

Keysight.write(":OUTP1 OFF")
Keysight.write(":OUTP2 OFF")

print('Measurement done.')
#figure(1);plot(freq/1e6,abs(traces))
#title(name)
#xlabel('Frequency [MHz]')
#ylabel('Magnitude [a.u.]')
