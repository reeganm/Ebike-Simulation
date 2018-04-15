# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:53:56 2018

@author: Reegan
"""

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

bike.battery.Voltage = 24.0


#plot motor characteristics
Ms = np.arange(0.0, 4000, 1)
I = bike.motor.CalcCurrent(RPM2radpers(Ms),bike.battery.Voltage)
plt.plot(Ms, I)
plt.xlabel('Speed (RPM)')
plt.ylabel('Current (A)')
plt.title('Motor Speed vs Current')
plt.grid(True)
plt.savefig("SpeedvsCurrent.out.png")
plt.show()

T = bike.motor.CalcTorque(I)
plt.plot(Ms, T)
plt.xlabel('Speed (RPM)')
plt.ylabel('Torque (Nm)')
plt.title('Motor Speed vs Torque at 24V')
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


plt.plot(mpers2kmperhr(Bs), bike.WheelDrag()*mpers2kmperhr(Bs)/mpers2kmperhr(Bs), '-b', label='Wheel Drag')
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