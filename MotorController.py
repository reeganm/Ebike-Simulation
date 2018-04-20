# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 15:37:30 2018

@author: Reegan
"""

class MotorController:
    
    def __init__(self):
        
        Efficiency = None
        
    def Voltage(self):
        return(self.NumberOfCells*self.CellVoltage)
        
        