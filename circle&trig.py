# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.patches import Circle
import math

fig,ax=plt.subplots()

e=Circle(xy=(0,0),radius=100,facecolor='None',edgecolor='black')
s=Circle(xy=(0,100),radius=5)

plt.plot([-100,100],[0,0],'k--')
plt.plot([0,0],[-100,100],'k--')

ax.add_artist(e)
ax.add_artist(s)

line_vert,=plt.plot([0],[0])
line_hor,=plt.plot([0],[0])
line_r,=plt.plot([0],[0])

ax.add_artist(line_vert)
ax.add_artist(line_hor)

plt.axis('equal')
ax.set_xlim(-200,200)
ax.set_ylim(-200,200)

def init():
    global s
    s.set_visible(False)
    
def update(i):
    s.set_visible(False)
    line_vert.set_visible(False)
    line_hor.set_visible(False)
    line_r.set_visible(False)
    
    x=100*math.sin(math.pi*i/200)
    y=100*math.cos(math.pi*i/200)
    
    s.center=(x,y)
    
    line_vert.set_xdata([x,x])
    line_vert.set_ydata([0,y])
    
    line_hor.set_xdata([0,x])
    line_hor.set_ydata([y,y])
    
    line_r.set_xdata([0,x])
    line_r.set_ydata([0,y])
    
    s.set_visible(True)
    line_vert.set_visible(True)
    line_hor.set_visible(True)
    line_r.set_visible(True)
    
ani=animation.FuncAnimation(fig=fig,init_func=init,repeat=True,func=update,interval=10,blit=False,frames=400)
plt.show()
    