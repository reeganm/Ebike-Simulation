# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 18:30:29 2018

@author: Reegan
"""

class Battery:
    
    def __init__(self):
        
        NumberOfCells = None
        
        CellVoltage = None
        
    def Voltage(self):
        return(self.NumberOfCells*self.CellVoltage)
        
        