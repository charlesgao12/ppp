# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.patches import Circle
import math

from matplotlib import animation


fig,ax=plt.subplots()

def focalpoint(fl,cam,x,y,z):
    sf = fl/(fl+z-cam[2])
    project_x=(x-cam[0])*sf
    project_y=(y-cam[1])*sf
    return project_x,project_y

def para_curve():
    ay=-0.1*np.ones(8)
    vx=np.sin(np.linspace(0,(360-45)*math.pi/180,8))
    vz=np.cos(np.linspace(0,(360-45)*math.pi/180,8))
    length=len(ay)
    
    lines=[None for i in range(length)]
    
    fl=100
    t=np.arange(100)
    cam=[0,50,-300]
    
    for i in range(length):
        x=vx[i]*t
        z=vz[i]*t
        y=ay[i]*t*t/2
        
        p_x,p_y=focalpoint(fl,cam,x,y,z)
        lines[i],=ax.plot(p_x,p_y)

para_curve()



plt.show()