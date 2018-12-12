# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import random

class ScatterFirework:
    def __init__(self,sca):
        self.scatter = sca
        
    explosion_length=30
    ay=-0.03
    number = random.randint(10,40)
    vx = np.random.uniform(-3,3,number)
    vy=np.random.uniform(1,4,number)
    
    size_base=0.01
    vy_start =10
    start_length =30
    
    explose_time =100
    explose_point=0,0
    
    col='#ffffff'
    
    start_x=0
    
    start_index=10
    first_time = True
    
    frame_len =250
    
    def init(self):
        pass#print('init')
    
    def rand_bright(self):
        return '#'+str(hex(random.randint(99,int(0xff))))[2:]+str(hex(random.randint(99,int(0xff))))[2:]+str(hex(random.randint(99,int(0xff))))[2:]
    
    def one_line(self,i,vx,vy,line_len,col):
        length = min(line_len,i)
        
        t=np.arange(length)
        if self.explosion_length <i:
            t=np.arange(i-length,i)
        
        x=self.explose_point[0]+t*vx
        y=self.explose_point[1]+(vy+self.ay*t)*t
        pos=np.stack((x,y),axis=-1)
        size=np.arange(length)*self.size_base
        color=np.full(length,col)
        return pos,size,color
    
    def explose(self,i):
        self.scatter.set_visible(False)
        pos,size,color=self.one_line(i,self.vx[0],self.vy[0],self.explosion_length,self.col)
        
        for j in range(1,self.number):
            new_line = self.one_line(i,self.vx[j],self.vy[j],self.explosion_length,self.col)
            pos=np.append(pos,new_line[0])
            size=np.append(size,new_line[1])
            color=np.append(color,new_line[2])
        
 
        self.scatter.set_offsets(pos)
        self.scatter.set_sizes(size)
        self.scatter.set_color(color)
        
        self.scatter.set_visible(True)
        
    def start(self,i):

        self.scatter.set_visible(False)
 
        length = min(self.start_length,i)
   
        t=np.arange(length)
        
        if length<i:
            t=np.arange(i-length,i)
        
        x=np.full(length,self.start_x)
        
        y=-600 +(self.vy_start+self.ay*t)*t
 
        
        pos=np.stack((x,y),axis=-1)
 
        size=np.arange(length)*0.1
        color=np.full(length,"#ffffff")

        self.scatter.set_offsets(pos)
        self.scatter.set_sizes(size)
        self.scatter.set_color(color)
        
        self.scatter.set_visible(True)
        
        return x[-1],y[-1]
    
    def update(self,i):
        #print('update',i)
        i = i-self.start_index
        
        if i<0 and self.first_time:
            pass
        elif i==0 and self.first_time:
            self.first_time=False
        elif i<0:
            i=self.frame_len+i
            
        if i==0:
            self.col=self.rand_bright()
            self.explosion_length=random.randint(5,30)
            self.number =random.randint(10,40)
            self.vx=4*np.random.random(self.number)-2
            self.vy=4*np.random.random(self.number)
            self.size_base=np.random.uniform(0.01,0.1)
            self.start_x=random.randint(-300,300)
            self.explose_time =random.randint(100,200)
            
        elif i<0:
            pass
        else:
            if i<self.explose_time:
                self.start(i)
            elif i==self.explose_time:
                self.explose_point=self.start(i)
                self.explose(i-self.explose_time)
            else:
                self.explose(i-self.explose_time)
                
fig,ax =plt.subplots()

ax.set_facecolor('black')

sca1=plt.scatter(0,0,c="#ffffff",s=1)
sca2=plt.scatter(0,0,c='#ffffff',s=1)
sca3=plt.scatter(0,0,c='#ffffff',s=1)
                 
a = ScatterFirework(sca1)
b = ScatterFirework(sca2)
c = ScatterFirework(sca3)
    
plt.xlim((-600,600))
plt.ylim((-800,800))  

ani=animation.FuncAnimation(fig=fig,init_func=a.init,repeat=True,func=a.update,interval=10,blit=False,frames=250)
ani2=animation.FuncAnimation(fig=fig,init_func=b.init,repeat=True,func=b.update,interval=10,blit=False,frames=250)
ani3=animation.FuncAnimation(fig=fig,init_func=c.init,repeat=True,func=c.update,interval=10,blit=False,frames=250)

plt.show()
        