# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:21:54 2018

@author: Reegan
"""

from Wheel import Wheel
from Motor import Motor
from Battery import Battery


#Bicycle Class
class Bike:
    """Class for modeling a bicycle"""
    
    #put any class variables here
    
    
    def __init__(self):
        """Initializes the data"""
        
        #create empty object properties
        self.mass = None
        
        self.wheel = Wheel()
        
        self.motor = Motor()
        
        self.GearRatio = None
        
        self.GearEfficieny = None
        
        self.Cd = None
        
        self.Af = None
        
        self.battery = Battery()
        
    def AirDrag(self,rho,v):
        return(0.5*rho*self.Cd*self.Af*v*v)
        
    def WheelDrag(self):
        #assumes normal force is always equal to gravity
        return(self.wheel.Crr*self.mass*9.81)

    def MotorSpeed2WheelSpeed(self,Speed):
        return(Speed/self.GearRatio)
        
    def WheelSpeed2BikeSpeed(self,Speed):
        return(Speed*self.wheel.Radius())
        
    def BikeSpeed2WheelSpeed(self,Speed):
        return(Speed/self.WheelSpeed2BikeSpeed(1))
        
    def WheelSpeed2MotorSpeed(self,Speed):
        return(Speed/self.MotorSpeed2WheelSpeed(1))
    
    def BikeSpeed2MotorSpeed(self,Speed):
        return(self.WheelSpeed2MotorSpeed(self.BikeSpeed2WheelSpeed(Speed)))

    def MotorSpeed2BikeSpeed(self,Speed):
        return(Speed/self.BikeSpeed2MotorSpeed(1))
        
    def MotorTorque2WheelTorque(self,MT):
        return(MT*self.GearRatio*self.GearEfficiency)
        

"""this function will run if Bike.py is run from a shell"""
def main():
    b = Bike()
    print(b)
    print(Wheel.Count())
    
if __name__ == "__main__":
    main()