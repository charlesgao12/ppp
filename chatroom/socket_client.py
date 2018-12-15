# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 14:32:11 2018

@author: chael
"""

import socket

from tkinter import Tk,Frame,Text,END,Button,PhotoImage,Label,S,scrolledtext
from time import strftime,localtime
import time

import threading
from collections import deque
 


class Client:

    msg_list =deque()
    
    soc = None
    
    callback = None

    def heartbeat(self):
        msg = "!!!"#heartbeat
        if len(self.msg_list) >0:
            msg = self.msg_list.popleft()
            
        print('now sending:'+msg)
        self.soc.sendall(bytes(msg, encoding="utf-8"))
    	



    #this just add msg to the deque
    def sendmsg(self,msg):
        print('add: '+msg)
        self.msg_list.append(msg)
        
        
    def handle(self,msg):
        self.callback(msg)
        
    def add_handler(self,cb):
        self.callback=cb
        
    
    def start_client(self):
        self.soc = socket.socket()
        
        self.soc.connect(("127.0.0.1",9000))
        
        ret_bytes = self.soc.recv(1024)
        ret_str = str(ret_bytes,encoding="utf-8")
        print('start: '+ret_str)
        
        while True:
            self.heartbeat()
        	

            #self.soc.sendall(bytes(inp, encoding="utf-8"))
            ret_bytes = self.soc.recv(1024)
            ret_str = str(ret_bytes,encoding="utf-8")
            print('received: '+ret_str)
            if ret_str == '!!!':#heartbeat
            	pass
            else:
            	self.handle(ret_str)
            time.sleep(0.01)
            

            


class Window:
    
    tk=Tk()
    
    soc_client = Client()
    
    def run_client(soc_client):
        soc_client.start_client()
        
    t=threading.Thread(target=run_client, args=(soc_client,))
    t.start()
    
    
    
    
    #frameLT = Frame(width=500, height=320)
    frameLC = Frame(width=500, height=150,bg="red")
    frameLB = Frame(width=500, height=30)
    frameRT = Frame(width=380, height=500)
    
    #txtMsgList=Text(frameLT)
    txtMsgList=scrolledtext.ScrolledText(width=70, height=25)
    txtMsg=Text(frameLC)
    

    def received(self,msg):
        strtime="小明："+strftime("%Y-%m-%d %H:%M:%S",localtime())+"\n"
        self.txtMsgList.insert(END,strtime,'bluecolor')
        #0.0是0行0列到END，表示全部，END表示插入末端
        self.txtMsgList.insert(END,msg)
        self.txtMsgList.see(END)#scroll to the end

 
    def sendMsg(self):
        strtime="我："+strftime("%Y-%m-%d %H:%M:%S",localtime())+"\n"
        self.txtMsgList.insert(END,strtime,'greencolor')
        #0.0是0行0列到END，表示全部，END表示插入末端
        self.txtMsgList.insert(END,self.txtMsg.get('0.0',END))
        self.soc_client.sendmsg(self.txtMsg.get('0.0',END))
        self.txtMsg.delete('0.0',END)
        self.txtMsgList.see(END)#scroll to the end
        
 
    def cancelMsg(self):
        self.txtMsg.delete('0.0',END)
 
    def sendMsgEvent(self,event):
        if event.keysym=="Return":
            self.sendMsg()
    def __init__(self):
        
        pass
    
    def add_handler(self, hdl):
        self.soc_client.add_handler(hdl)
        
    def start(self):
        self.tk.title("千里马聊天室-小红")
        # 创建frame容器
        
     
        #创建控件
        
        #配置标签tag的属性，第一个参数为tag名字，第2个参数为前景色，背景色为默认白色
        self.txtMsgList.tag_config("greencolor", foreground='#008C00')
        
        self.txtMsg.bind_all("<KeyPress-Return>",self.sendMsgEvent)
        btnSend=Button(self.frameLB,text="send",width=8,command=self.sendMsg)
        btnCancel=Button(self.frameLB,text="cancel",width=8,command=self.cancelMsg)
        myImage=PhotoImage(file="chat.PNG")
        label=Label(self.frameRT,image=myImage)
        charimg=PhotoImage(file="hong.PNG")
        label1=Label(self.frameRT,image=charimg)
     
        #窗体布局
        #self.frameLT.grid(row=0, column=0, columnspan=2,padx=1,pady=5)
        self.txtMsgList.grid(row=0, column=0, columnspan=2,padx=1,pady=5)
        self.frameLC.grid(row=1, column=0, columnspan=2)
        self.frameLB.grid(row=2, column=0, columnspan=2)
        self.frameRT.grid(row=0, column=2, rowspan=3,padx=5,pady=4)
     
        # 固定大小
        #self.frameLT.grid_propagate(0)
        self.frameLC.grid_propagate(0)
        self.frameLB.grid_propagate(0)
        self.frameRT.grid_propagate(0)
     
        #控件布局
        btnSend.grid(row=2, column=0)
        btnCancel.grid(row=2, column=1)
        label.grid(sticky=S)
        label1.grid(sticky=S)
        self.txtMsgList.grid()
        self.txtMsg.grid()
     
        #主事件循环
        self.tk.mainloop()
        
print('start tk')        
window =Window()
def handle_msg(msg):
    print('tk received: '+msg)
    window.received(msg)
    
window.add_handler(handle_msg)

window.start()
