# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 17:48:53 2018

@author: Reegan
"""

import math

def in2m(x):
    return(x*25.4/1000)
    
def lb2kg(x):
    return(x*0.453592)
    
def RPMperV2radperVs(x):
    return(x/60*2*math.pi)
    
def RPM2radpers(x):
    return(x/60*2*math.pi)

def radpers2RPM(x):
    return(x/RPM2radpers(1))
    
def mpers2kmperhr(x):
    return(x*3.6)