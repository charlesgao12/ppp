# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.patches import Circle
import math




fig,ax=plt.subplots()

def focalpoint(fl,cam,x,y,z):
    sf = fl/(fl+z-cam[2])
    project_x=(x-cam[0])*sf
    project_y=(y-cam[1])*sf
    return project_x,project_y

cam=[0,50,-300]

ay=-0.1*np.ones(8)
vx=np.sin(np.linspace(0,(360-45)*math.pi/180,8))
vz=np.cos(np.linspace(0,(360-45)*math.pi/180,8))
length=len(ay)

lines=[None for i in range(length)]

fl=100
t=np.arange(100)


for i in range(length):
    x=vx[i]*t
    z=vz[i]*t
    y=ay[i]*t*t/2
    
    p_x,p_y=focalpoint(fl,cam,x,y,z)
    lines[i],=ax.plot(p_x,p_y)



def init():
    pass


def update(i):
    global cam
    
    cam_x = 300*math.sin(i*math.pi/180)
    cam_z = 300*math.cos(i*math.pi/180)
    cam=[cam_x,50,cam_z]
    
    t=np.arange(100)
    
    for i in range(length):
        x=vx[i]*t
        z=vz[i]*t
        y=ay[i]*t*t/2
        
        p_x,p_y=focalpoint(fl,cam,x,y,z)
        lines[i].set_xdata(p_x)
        lines[i].set_ydata(p_y)
    
    
    

plt.xlim((-200,200))
plt.ylim((-200,200))

ani=animation.FuncAnimation(fig=fig,init_func=init,repeat=True,func=update,interval=30,blit=False,frames=2000)


plt.show()