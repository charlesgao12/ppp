# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import random

fig,ax=plt.subplots()
ax.set_facecolor('black')

explosion_length=30
ay=-0.03
number=random.randint(10,20)
vx =np.random.uniform(-3,3,number)
vy =np.random.uniform(1,4,number)
scatter =plt.scatter(0,0,c='white',s=1)

plt.xlim((-600,600))
plt.ylim((-800,800))

def init():
    global x,y
    x=[0]
    y=[0]
    
def one_line(i,vx,vy):
    length =min(explosion_length,i)
    t=np.arange(length)
    if explosion_length<i:
        t=np.arange(i-length,i)
        
    x=explose_point[0]+t*vx
    y=explose_point[1]+(vy+ay*t)*t
    
    pos=np.stack((x,y),axis=-1)
    size=np.arange(length)*0.01
    color=np.full(length,'white')
    
    return pos,size,color

def explose(i):
    global vx,vy,number
    
    if i==0:
        number=random.randint(15,20)
        vx=(2+2)*np.random.random(number)-2
        vy=4*np.random.random(number)
        
    scatter.set_visible(False)
    
    pos,size,color=one_line(i,vx[0],vy[0])
    
    for j in range(1,number):
        new_line=one_line(i,vx[j],vy[j])
        pos=np.append(pos,new_line[0])
        size=np.append(size,new_line[1])
        color=np.append(color,new_line[2])
      
    print(pos)
    scatter.set_offsets(pos)
    scatter.set_sizes(size)
    scatter.set_color(color)
    
    scatter.set_visible(True)
    
vy_start=10
start_length=30

def start(i):
    scatter.set_visible(False)
    
    length=min(start_length,i)
    
    t=np.arange(length)
    if start_length<i:
        t=np.arange(i-length,i)
        
    x=np.zeros(length)
    y=-600 +(vy_start+ay*t)*t
    pos=np.stack((x,y),axis=-1)
    size=np.arange(length)*0.1
    color=np.full(length,'white')
    scatter.set_offsets(pos)
    scatter.set_sizes(size)
    scatter.set_color(color)
    scatter.set_visible(True)
    
    return x[-1],y[-1]

explose_time=100
explose_point=0,0

def update(i):
    if i<explose_time:
        start(i)
    elif i==explose_time:
        global explose_point
        explose_point =start(i)
        explose(i-explose_time)
    else:
        explose(i-explose_time)
        

ani=animation.FuncAnimation(fig=fig,init_func=init,repeat=True,func=update,interval=10,blit=False,frames=250)
plt.show()
    