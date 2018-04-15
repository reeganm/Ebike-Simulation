# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:29:38 2018

@author: Reegan
"""

import math

class Wheel:
    """Class describing a bicycle wheel"""
    
    #put any class variables here
    Number = 0
    
    def __init__(self):
        
        #object properties
        
        #wheel diameter
        self.Diameter = None
        
        #rolling resistance coefficient
        self.Crr = None
        
        #add 1 to number of wheels
        Wheel.Number += 1
        
    def Radius(self):
        return(self.Diameter/2)
        
    def Circumference(self):
        return(self.Diameter*math.pi)
        
    @classmethod 
    def Count(cls):
        return(cls.Number)
        
"""this function will run if Bike.py is run from a shell"""
def main():
    w = Wheel()
    print(w)
    
if __name__ == "__main__":
    main()