# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 14:31:28 2018

@author: chael
"""

import  socketserver

from tkinter import Tk,Frame,Text,END,Button,PhotoImage,Label,S,scrolledtext
from time import strftime,localtime

import threading
from collections import deque

class Controller:
    msg_list =deque()
    def add_handler(self,hdl):
        self.handler = hdl
    
    def received(self,msg):
        #print('received:'+msg)
        msg_out = '!!!'
        if msg == '!!!':#heartbeat, see if any msg need to send
            if len(self.msg_list) >0:
                msg_out =  self.msg_list.popleft()           
        else:
            self.handler(msg)

        self.conn.sendall(bytes(msg_out,encoding="utf-8"))
        #print('sent:'+msg_out)
        
        
    def sendmsg(self,msg):
        self.msg_list.append(msg)
        
        
    def set_conn(self,con):
        self.conn=con

            
class Myserver:     

        
    def start(self,ctrl):        
        class Handler(socketserver.BaseRequestHandler):      
        
            def handle(self):
                conn = self.request
                ctrl.set_conn(conn)
                conn.sendall(bytes("success connected",encoding="utf-8"))
                while True:
                    ret_bytes = conn.recv(1024)
                    ret_str = str(ret_bytes,encoding="utf-8")
                    ctrl.received(ret_str)
                    
        
        
        server = socketserver.ThreadingTCPServer(("0.0.0.0",9000),Handler)
        server.serve_forever()
    
    
class Window:
    
    tk=Tk()
    
    soc_serv = Myserver()
    
    ctrl = Controller()
    
    def run_serv(soc_serv,ctrl):
        soc_serv.start(ctrl)
        
    t=threading.Thread(target=run_serv, args=(soc_serv,ctrl))
    t.start()
    
    
    
    
    #frameLT = Frame(width=500, height=320)
    frameLC = Frame(width=500, height=150,bg="red")
    frameLB = Frame(width=500, height=30)
    frameRT = Frame(width=380, height=500)
    
    txtMsgList=scrolledtext.ScrolledText(width=70, height=25)
    
    
   
    
    txtMsg=Text(frameLC)
    

    def received(self,msg):
        strtime="小红："+strftime("%Y-%m-%d %H:%M:%S",localtime())+"\n"
        self.txtMsgList.insert(END,strtime,'bluecolor')
        #0.0是0行0列到END，表示全部，END表示插入末端
        self.txtMsgList.insert(END,msg)
        self.txtMsgList.see(END)#scroll to the end
        

 
    def sendMsg(self):
        strtime="我："+strftime("%Y-%m-%d %H:%M:%S",localtime())+"\n"
        self.txtMsgList.insert(END,strtime,'greencolor')
        #0.0是0行0列到END，表示全部，END表示插入末端
        self.txtMsgList.insert(END,self.txtMsg.get('0.0',END))
        self.ctrl.sendmsg(self.txtMsg.get('0.0',END))
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
        self.ctrl.add_handler(hdl)
        
    def start(self):
        self.tk.title("千里马聊天室-小明")
        # 创建frame容器
        
     
        #创建控件
        
        #配置标签tag的属性，第一个参数为tag名字，第2个参数为前景色，背景色为默认白色
        self.txtMsgList.tag_config("greencolor", foreground='#008C00')
        
        self.txtMsg.bind_all("<KeyPress-Return>",self.sendMsgEvent)
        btnSend=Button(self.frameLB,text="send",width=8,command=self.sendMsg)
        btnCancel=Button(self.frameLB,text="cancel",width=8,command=self.cancelMsg)
        myImage=PhotoImage(file="chat.PNG")
        label=Label(self.frameRT,image=myImage)
        
        charimg=PhotoImage(file="ming.PNG")
        label1=Label(self.frameRT,image=charimg)
     
        #窗体布局
        #self.frameLT.grid(row=0, column=0, columnspan=2,padx=1,pady=5)
        self.txtMsgList.grid(row=0, column=0, columnspan=2,padx=1,pady=5)
        self.frameLC.grid(row=1, column=0, columnspan=2)
        self.frameLB.grid(row=2, column=0, columnspan=2)
        self.frameRT.grid(row=0, column=2, rowspan=3,padx=5,pady=4)
     
        # 固定大小
        #self.frameLT.grid_propagate(0)
        #self.txtMsgList.grid_propagate(0)
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
    #print('tk received: '+msg)
    window.received(msg)
    
window.add_handler(handle_msg)

window.start()