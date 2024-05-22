# -*- coding: utf-8 -*-
"""
Created on Fri May 17 23:43:24 2024

@author: hpopo
"""
import numpy as np
from matplotlib import pyplot as plt

wave_lat=40.920269

wave_long=-83.565529

time=180 #seconds

temp = 216.69 #kelvin


def sos(T):
    gamma = 1.4
    R = 8.31 #J/mol*K
    M = 0.02897 #kg/mol
    return np.sqrt(gamma*R*T/M)

speed=sos(temp)

d=speed*time

fig,ax = plt.subplots()
ax.scatter(wave_long,wave_lat)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

wave_lat2=[]
wave_long2=[]

for i in range(0,360):
    wave_lat2.append(wave_lat+d*np.cos((np.radians(i)))/111111)
    wave_long2.append(wave_long+d*np.sin((np.radians(i)))/np.cos(wave_lat2[i])/111111)
ax.scatter(wave_long2,wave_lat2)
plt.show()

coords=np.array((wave_lat2,wave_long2))