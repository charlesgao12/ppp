# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.patches import Circle
import math
from matplotlib import animation

fig,ax=plt.subplots()
def init():
    pass

fl =2
def update(i):
    fl = -3+ i
    rec(fl)
    
def focalpoint(fl,cam,i):
    sf = fl/(fl+i[2]-cam[2])
    project_x=(i[0]-cam[0])*sf
    project_y=(i[1]-cam[1])*sf
    return project_x,project_y

cross = [None,None,None,None]
inner = None
outer = None

def rec(fl):
    cam=[2,3,-4]
    
    points=[(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
    
    
    points_project=[focalpoint(fl,cam,i) for i in points]
    x1=[i[0] for i in points_project[0:4]]
    y1=[i[1] for i in points_project[0:4]]
    x2=[i[0] for i in points_project[4:]]
    y2=[i[1] for i in points_project[4:]]
    
    x1=np.append(x1,x1[0])
    y1=np.append(y1,y1[0])
    x2=np.append(x2,x2[0])
    y2=np.append(y2,y2[0])
    
    global cross,inner,outer
    
    for i in range(4):
        #z=plt.plot([x1[i],x2[i]],[y1[i],y2[i]],'k-')
        #print(z[0])
        
        if cross[i] == None:
            cross[i]=plt.plot([x1[i],x2[i]],[y1[i],y2[i]],'k-')
        else:
            cross[i][0].set_xdata([x1[i],x2[i]])
            cross[i][0].set_ydata([y1[i],y2[i]])
        
            
    if inner == None:
        inner=plt.plot(x1,y1)
    else:
        inner[0].set_xdata(x1)
        inner[0].set_ydata(y1)
        
    if outer == None:
        outer= plt.plot(x2,y2)
    else:
        outer[0].set_xdata(x2)
        outer[0].set_ydata(y2)
    '''   
    a=plt.plot(x1,y1)
    b=plt.plot(x2,y2)
    
    print(a[0])
    print(b[0])
    '''
        
    
    
    
    
plt.xlim((-2,2))
plt.ylim((-2,2))

ani=animation.FuncAnimation(fig=fig,init_func=init,repeat=True,func=update,interval=1000,blit=False,frames=20)


plt.show()