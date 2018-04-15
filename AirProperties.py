# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:55:05 2018

@author: Reegan
"""


#https://www.engineeringtoolbox.com/air-density-specific-weight-d_600.html
#polynomial fit taken from javascript code. Accuracy withing 0.2%
def Density(Tc):
    rho = 0.00000000000000029576*Tc*Tc*Tc*Tc*Tc*Tc-0.00000000000039652642*Tc*Tc*Tc*Tc*Tc+0.00000000021718680185*Tc*Tc*Tc*Tc-0.00000006945751260987*Tc*Tc*Tc+0.0000178311601969631*Tc*Tc-0.00471854397898636*Tc+1.29163880414105
    return(rho)