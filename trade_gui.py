# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 20:08:05 2022

@author: admin
"""
from xueqiu_spider_gui2 import *

import tkinter 
from tkinter import Listbox
from tkinter import Button
from tkinter import Checkbutton
from tkinter import Label
from tkinter import messagebox
from tkinter import Frame
from tkinter import Entry
from tkinter import *
import threading
import inspect
import ctypes

#
#class trade_wrapper():
#    def __init__(self,max_time_diff=120,filename="test1.txt",cmd_file="command.csv",workmode_en=1 , workdir ="C:\\Users",init_en=0,tampfile="tamp.txt",sleeptime=10 ):
#            
def stop_thread(thread, exctype=SystemExit):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(thread.ident)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

    ####init 
t_list=[]
root = tkinter.Tk()# 初始化
max_time_diff =120 # df['max_time_diff'][0] ####文本框
filename      ='test1.txt' # df['filename'][0]  ####文本框
cmd_file      ='command.csv' # df['cmd_file'][0]  ####文本框
workdir       ='D:\\testfile1' # df['workdir'][0]  ####文本框
sleeptime     =10# df['sleeptime'][0]  ####文本框
tampfile      ='tamp.txt' # df['tampfile'][0]   ####文本框
init_en       =0 # df['init_en'][0]  ##选择框 ## init or follower
workmode_en   =1 # df['workmode_en'][0] # 选择框，调试 or work

width = 300
height = 480
# 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
#选择栏

###模式选择
def CallOn(event):
    root1=tkinter.Tk()
    Label(root1,text='你的选择是'+lb.get(lb.curselection()) + '  ').pack()
    Button(root1,text='确认',command=root1.destroy).pack()
    #print (lb.get(lb.curselection()))
    global workmode_en
    if (lb.get(lb.curselection())=='调试模式'  ):        
        workmode_en=0
        print("调试模式,workmode_en=%d" % (workmode_en))
      
    else:
        workmode_en=1
        print("工作模式")


###################################################################################
### intt or follower
def CallOn1(event):
    root1=tkinter.Tk()
    Label(root1,text='你的选择是'+lb1.get(lb1.curselection()) + '  ').pack()
    Button(root1,text='确认',command=root1.destroy).pack()
    #print (lb1.get(lb1.curselection()))
    global init_en
    if (lb1.get(lb1.curselection())=='仓位复制'  ):
        init_en = 1
        print("仓位复制")
    else:
        init_en = 0
        print("follow最新调仓")

def getuser1():
  user=user_text1.get() #获取文本框内容
  print (user)
  global max_time_diff
  max_time_diff = int(user) 
  
def getuser2():
  user=user_text2.get() #获取文本框内容
  print (user)
  global filename
  filename =user

def getuser3():
  user=user_text3.get() #获取文本框内容
  print (user)
  global cmd_file
  cmd_file=user

def getuser4():
  user=user_text4.get() #获取文本框内容
  print (user)
  global workdir
  workdir=user

def getuser5():
  user=user_text5.get() #获取文本框内容
  print (user)
  global sleeptime
  sleeptime=int(user) 

def getuser6():
  user=user_text6.get() #获取文本框内容
  print (user)
  global tampfile
  tampfile=user

def hit_me():
    messagebox.showinfo(title='提示', message='start')
    print("start")
    ########
    u0 =trade_wrapper(workmode_en=workmode_en,max_time_diff=max_time_diff,cmd_file=cmd_file,workdir=workdir,filename=filename,init_en=init_en,tampfile=tampfile,sleeptime=sleeptime)


    thread = threading.Thread(target=u0.process)  ###将主程序放入子线程，
    thread.start()
    global t_list
    t_list.append(thread)
    
def hit_me1():
    messagebox.showinfo(title='提示', message='stop')
    print("stop")
    import sys
    for i in t_list:
        stop_thread(i)
        print("stop sun thread i=%s" % (i))
      
    root.destroy()
    sys.exit()
    
 
  
#def run(self):
lb = Listbox(root,height=2)
#双击命令
lb.bind('<Double-Button-1>',CallOn)
for i in ['调试模式','工作模式']:
    lb.insert(END,i)
lb.pack()

lb1 = Listbox(root,height=2)
#双击命令
lb1.bind('<Double-Button-1>',CallOn1)
for i in ['仓位复制','follow最新调仓']:
    lb1.insert(END,i)
lb1.pack()

####文本框
##max_time_diff
v1 = StringVar()
user_text1=tkinter.Entry(textvariable=v1) #创建文本框
user_text1.pack()
v1.set("120")
tkinter.Button(root,text="max time diff(s)",command=getuser1).pack() #command绑定获取文本框内容方法

##max_time_diff
v2 = StringVar()
user_text2=tkinter.Entry(textvariable=v2) #创建文本框
user_text2.pack()
v2.set("test1.txt")
tkinter.Button(root,text="下单保存文件",command=getuser2).pack() #command绑定获取文本框内容方法

##max_time_diff
v3 = StringVar()
user_text3=tkinter.Entry(textvariable=v3) #创建文本框
user_text3.pack()
v3.set("command.csv")
tkinter.Button(root,text="cookies file",command=getuser3).pack() #command绑定获取文本框内容方法


##max_time_diff
v4 = StringVar()
user_text4=tkinter.Entry(textvariable=v4) #创建文本框
user_text4.pack()
v4.set("D:\\testfile1")
tkinter.Button(root,text="工作目录",command=getuser4).pack() #command绑定获取文本框内容方法


##max_time_diff
v5 = StringVar()
user_text5=tkinter.Entry(textvariable=v5) #创建文本框
user_text5.pack()
v5.set("10")
tkinter.Button(root,text="交易间隔(s)",command=getuser5).pack() #command绑定获取文本框内容方法

##max_time_diff
v6 = StringVar()
user_text6=tkinter.Entry(textvariable=v6) #创建文本框
user_text6.pack()
v6.set("tamp.txt")
tkinter.Button(root,text="时间戳文件",command=getuser6).pack() #command绑定获取文本框内容方法

#####start
frame = Frame(root)
frame.pack()
button = Button(frame, text='start', bg='green',width=10 , command=hit_me)
button.pack()

###stop
frame1 = Frame(root)
frame1.pack()
button1 = Button(frame1, text='stop', bg='green',width=10 , command=hit_me1)
button1.pack()
#####################################################

#####################################################
root.mainloop()
# #####################################################################################
        