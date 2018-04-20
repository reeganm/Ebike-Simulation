# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:53:56 2018

@author: Reegan
"""

import sys
import copy
import matplotlib.pyplot as plt
import numpy as np
from Bike import Bike
from AirProperties import Density
from UnitConversionLib import in2m, lb2kg, RPMperV2radperVs, RPM2radpers, mpers2kmperhr
from UnitConversionLib import radpers2RPM

#air temperature
T = 20 #C

#air density
rho = Density(20);

#create a bike object
bike = Bike()

bike.mass = lb2kg(200) 

bike.wheel.Diameter = in2m(26)

#https://www.engineeringtoolbox.com/rolling-friction-resistance-d_1303.html
bike.wheel.Crr = 0.008 #rough paved road

#https://www.engineeringtoolbox.com/drag-coefficient-d_627.html
bike.Cd = 1.1 #upright commuter

#https://www.cyclingpowerlab.com/CyclingAerodynamics.aspx
bike.Af = 0.6 #m^2

#estimated from https://www.l-faster.com/items/450w-electric-common-bike-motor-kit-side-drive/
bike.motor.kt = 0.05789 #Nm/A
bike.motor.kV = RPMperV2radperVs(166.6666)
bike.motor.R = 0.243 #ohm

bike.GearRatio = 7.18
bike.GearEfficiency = 0.9

bike.battery.NumberOfCells = 6
bike.battery.CellVoltage = 3.2 #a 3V battery is dead. 4.2 is full

print('Bike object size ' + str(sys.getsizeof(bike)) + ' B')


## Steady State Calculation ##

#plot motor characteristics
Ms = np.arange(0.0, 4000, 0.01)
I = bike.motor.CalcCurrent(RPM2radpers(Ms),bike.battery.Voltage())
plt.plot(Ms, I)
plt.xlabel('Speed (RPM)')
plt.ylabel('Current (A)')
plt.title('Motor Speed vs Current at ' + str(round(bike.battery.Voltage(),3)) + ' V')
plt.grid(True)
plt.savefig("SpeedvsCurrent.out.png")
plt.show()

T = bike.motor.CalcTorque(I)
plt.plot(Ms, T)
plt.xlabel('Speed (RPM)')
plt.ylabel('Torque (Nm)')
plt.title('Motor Speed vs Torque at ' + str(round(bike.battery.Voltage(),3)) + ' V')
plt.grid(True)
plt.savefig("SpeedvsTorque.out.png")
plt.show()

#plot bike torque speed characteristics
Bs = bike.MotorSpeed2BikeSpeed(RPM2radpers(Ms))
WT = bike.MotorTorque2WheelTorque(T)
plt.plot(mpers2kmperhr(Bs), WT)
plt.xlabel('Speed (kph)')
plt.ylabel('Torque at Wheel (Nm)')
plt.title('Torque at Wheel vs Bike Speed')
plt.grid(True)
plt.savefig("BikeSpeedvsWheelTorque.out.png")
plt.show()


plt.plot(mpers2kmperhr(Bs), bike.WheelDrag()*np.ones(Bs.shape), '-b', label='Wheel Drag')
plt.plot(mpers2kmperhr(Bs), bike.AirDrag(rho,Bs), '-r', label='Air Drag')
plt.xlabel('Speed (kph)')
plt.ylabel('Force (N)')
plt.legend(loc='upper right')
plt.title('Drag Components')
plt.grid(True)
plt.savefig("DragvsSpeed.out.png")
plt.show()

Fd = bike.AirDrag(rho,Bs) + bike.WheelDrag()
Fw = WT/bike.wheel.Radius()
plt.plot(mpers2kmperhr(Bs), Fd, '-b', label='Drag')
plt.plot(mpers2kmperhr(Bs), Fw, '-r', label='Wheel')
plt.xlabel('Speed (kph)')
plt.ylabel('Force (N)')
plt.legend(loc='upper right')
plt.title('Steady State Force vs Speed')
plt.grid(True)
plt.savefig("SteadyStateForcevsSpeed.out.png")
plt.show()

print('Predicted max speed is where the wheel force meets the drag force')
i1 = np.argwhere((Fw-Fd)<=0)[0]

print('Max Speed = ' + str(round(np.asscalar(mpers2kmperhr(Bs[i1])),1)) + ' km/hr')

## Transient Simulation ##

bike.motor.MaxCurrent = 25 #lipos are limited to 15 A

NumberOfSteps = 240000
ts = 0.001

print('Simulation time: ' + str(NumberOfSteps*ts) + ' s')

t = np.arange(0.0, NumberOfSteps*ts, ts, dtype=np.float64) #time
p = np.zeros(NumberOfSteps, dtype=np.float64) #position
bs = np.zeros(NumberOfSteps, dtype=np.float64) #bike speed
ws = np.zeros(NumberOfSteps, dtype=np.float64) #wheel speed
ms = np.zeros(NumberOfSteps, dtype=np.float64) #motor speed
ba = np.zeros(NumberOfSteps, dtype=np.float64) #bike acceleration
wa = np.zeros(NumberOfSteps, dtype=np.float64) #wheel acceleration
ma = np.zeros(NumberOfSteps, dtype=np.float64) #motor acceleration
ad = np.zeros(NumberOfSteps, dtype=np.float64) #air drag
td = np.zeros(NumberOfSteps, dtype=np.float64) #total drag
mt = np.zeros(NumberOfSteps, dtype=np.float64) #motor torque
wt = np.zeros(NumberOfSteps, dtype=np.float64) #wheel torque
mc = np.zeros(NumberOfSteps, dtype=np.float64) #motor current
df = np.zeros(NumberOfSteps, dtype=np.float64) #drive force

totalmem = sys.getsizeof(t)+sys.getsizeof(p)+sys.getsizeof(bs)
totalmem += sys.getsizeof(ws)+sys.getsizeof(ms)+sys.getsizeof(ba)
totalmem += sys.getsizeof(wa)+sys.getsizeof(ma)+sys.getsizeof(ad)
totalmem += sys.getsizeof(td)+sys.getsizeof(mt)+sys.getsizeof(wt)
totalmem += sys.getsizeof(mc)+sys.getsizeof(df)

print('Total simulation memory usage: ' + str(round(totalmem/1024,2)) + ' kiB')

#initial conditions
bs[0] = 0
ws[0] = bike.BikeSpeed2WheelSpeed(bs[0])
ms[0] = bike.BikeSpeed2MotorSpeed(bs[0])

p[0] = 0

mc[0] = bike.motor.CalcCurrent(ms[0],bike.battery.Voltage())
if mc[0] > bike.motor.MaxCurrent:
    mc[0] = bike.motor.MaxCurrent
mt[0] = bike.motor.CalcTorque(mc[0])
wt[0] = bike.MotorTorque2WheelTorque(mt[0])
df[0] = wt[0]/bike.wheel.Radius()

ad[0] = bike.AirDrag(rho,bs[0])
td[0] = ad[0] + bike.WheelDrag()

ba[0] = (df[0] - td[0])/bike.mass

wa[0] = bike.BikeSpeed2WheelSpeed(ba[0])
ma[0] = bike.BikeSpeed2MotorSpeed(ba[0])

for i in np.arange(1,NumberOfSteps):
    #update conditions
    bs[i] = bs[i-1] + ba[i-1]*ts
    ws[i] = bike.BikeSpeed2WheelSpeed(bs[i])
    ms[i] = bike.BikeSpeed2MotorSpeed(bs[i])

    p[i] = p[i-1] + bs[i-1]*ts

    mc[i] = bike.motor.CalcCurrent(ms[i],bike.battery.Voltage())
    if mc[i] > bike.motor.MaxCurrent:
        mc[i] = bike.motor.MaxCurrent
    mt[i] = bike.motor.CalcTorque(mc[i])
    wt[i] = bike.MotorTorque2WheelTorque(mt[i])
    df[i] = wt[i]/bike.wheel.Radius()

    ad[i] = bike.AirDrag(rho,bs[i])
    td[i] = ad[i] + bike.WheelDrag()

    ba[i] = (df[i] - td[i])/bike.mass

    wa[i] = bike.BikeSpeed2WheelSpeed(ba[i])
    ma[i] = bike.BikeSpeed2MotorSpeed(ba[i])
    
# make some plots
    
plt.plot(t,mpers2kmperhr(bs))
plt.xlabel('Time (s)')
plt.ylabel('Bike Speed (kph)')
plt.title('Speed vs Time')
plt.grid(True)
plt.savefig("SpeedvTime.out.png")
plt.show()

plt.plot(t,mc)
plt.xlabel('Time (s)')
plt.ylabel('Motor Current (A)')
plt.title('Motor Current vs Time')
plt.grid(True)
plt.savefig("MotorCurrentvTime.out.png")
plt.show()

plt.plot(t, td, '-b', label='Total Drag')
plt.plot(t, ad, '-r', label='Air Drag')
plt.xlabel('Time (s)')
plt.ylabel('Drag (N)')
plt.legend(loc='upper right')
plt.title('Drag Components')
plt.grid(True)
plt.savefig("Dragvstime.out.png")
plt.show()