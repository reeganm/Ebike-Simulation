# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:39:43 2018

@author: Reegan
"""

class Motor:
    
    Number = 0
    
    def __init__(self):
        
        Motor.Number += 1
        
        self.kt = None #Nm/A
        self.kV = None #rad/s/V
        self.Resistance = None #ohm
        self.MaxCurrent = None
        
    def CalcCurrent(self,Speed,Voltage):
        return((Voltage-Speed/self.kV)/self.R)
        
    def CalcTorque(self,Current):
        return(Current*self.kt)
        
    @classmethod
    def Count(cls):
        return(cls.Number)
        