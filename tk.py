# -*- coding: utf-8 -*-
from tkinter import Tk,Frame,Text,END,Button,PhotoImage,Label,S
from time import strftime,localtime



 
class Window:
    
    tk=Tk()
    
    frameLT = Frame(width=500, height=320)
    frameLC = Frame(width=500, height=150,bg="red")
    frameLB = Frame(width=500, height=30)
    frameRT = Frame(width=380, height=500)
    
    txtMsgList=Text(frameLT)
    txtMsg=Text(frameLC)
 
    def sendMsg(self):
        strtime="我："+strftime("%Y-%m-%d %H:%M:%S",localtime())+"\n"
        self.txtMsgList.insert(END,strtime,'greencolor')
        #0.0是0行0列到END，表示全部，END表示插入末端
        self.txtMsgList.insert(END,self.txtMsg.get('0.0',END))
        self.txtMsg.delete('0.0',END)
 
    def cancelMsg(self):
        self.txtMsg.delete('0.0',END)
 
    def sendMsgEvent(self,event):
        if event.keysym=="Return":
            self.sendMsg()
    def __init__(self):
        
        pass
        
    def start(self):
        self.tk.title("千里马聊天室")
        # 创建frame容器
        
     
        #创建控件
        
        #配置标签tag的属性，第一个参数为tag名字，第2个参数为前景色，背景色为默认白色
        self.txtMsgList.tag_config("greencolor", foreground='#008C00')
        
        self.txtMsg.bind_all("<KeyPress-Return>",self.sendMsgEvent)
        btnSend=Button(self.frameLB,text="send",width=8,command=self.sendMsg)
        btnCancel=Button(self.frameLB,text="cancel",width=8,command=self.cancelMsg)
        myImage=PhotoImage(file="chat.PNG")
        label=Label(self.frameRT,image=myImage)
     
        #窗体布局
        self.frameLT.grid(row=0, column=0, columnspan=2,padx=1,pady=5)
        self.frameLC.grid(row=1, column=0, columnspan=2)
        self.frameLB.grid(row=2, column=0, columnspan=2)
        self.frameRT.grid(row=0, column=2, rowspan=3,padx=5,pady=4)
     
        # 固定大小
        self.frameLT.grid_propagate(0)
        self.frameLC.grid_propagate(0)
        self.frameLB.grid_propagate(0)
        self.frameRT.grid_propagate(0)
     
        #控件布局
        btnSend.grid(row=2, column=0)
        btnCancel.grid(row=2, column=1)
        label.grid(sticky=S)
        self.txtMsgList.grid()
        self.txtMsg.grid()
     
        #主事件循环
        self.tk.mainloop()

window =Window()
window.start()


