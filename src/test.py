#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import time
import threading

import Tkinter as tk


'''
def on_find(): 
  t2 = tk.Toplevel(root) 
  t2.title('Find') 
  t2.geometry('262x65+200+250') 


  t2.transient(root) 

  tk.Label(t2, text="Find All:").grid(row=0, column=0, sticky='e') 
  v= tk.StringVar() 
  e = tk.Entry(t2, width=25, textvariable=v) 
  e.grid(row=0, column=1, padx=2, pady=2, sticky='we') 
  e.focus_set() 
  c = tk.IntVar() 
  tk.Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2) 
  tk.Button(t2, text="Find All", underline=0,  command=lambda: 
  tk.search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=2) 

def close_search(): 
  tk.textPad.tag_remove('match', '1.0', END) 
  t2.destroy() 
  t2.protocol('WM_DELETE_WINDOW', close_search)   #override close 

#root = tk.Tk()

#for i in range(10):
  ##side
  #btn = tk.Button(text=i)
  #btn.pack(side="left")
  #btn.pack(side="right")

  ####fill
  #btn.pack(fill="x")
  #btn.pack(side="left",fill="y")
  #btn.pack(fill="both")

  ##expand
  #btn1 = tk.Button( text=1, bg="green")
  #btn2 = tk.Button( text=2, bg='yellow')
  #btn1.pack(fill="x")
  #btn2.pack(expand="true")

  #anchor:
  #btn1 = tk.Button(text=1,bg='green')
  #btn2 = tk.Button(text=2,bg='yellow')
  #btn1.pack(fill="x")
  #btn2.pack(anchor="e")
  
  
  #pack_propagete  # tell frame not to let its children control its size  
  #btn1 = tk.Button(text=1, bg='green')
  #btn2 = tk.Button(text=2, bg='yellow')
  #root.pack_propagate(0)
  #btn1.pack()
  #btn2.pack()
  
#pack_forget:


root = tk.Tk() 

for i in range(20):
  for j in range(15):
    tk.Label(root,text=10000,relief='sunken', bd='1px').grid(row=i,column=j,padx=0,pady=0)


    #self.pack(fill='x', expand='no')

root.mainloop()


root = tk.Tk()
tk.Button(root,text='A').pack(side='left',expand='yes',fill='y')
tk.Button(root,text='B').pack(side='top',expand='yes',fill='both')
tk.Button(root,text='C').pack(side='right',expand='yes',fill='none')
tk.Button(root,text='D').pack(side='left',expand='no',fill='y')
tk.Button(root,text='E').pack(side='top',expand='yes',fill='both')
tk.Button(root,text='F').pack(side='bottom',expand='yes')
tk.Button(root,text='G').pack(anchor='se')

root.mainloop()

'''


'''紧耦合'''
# 弹窗
class PopupDialog(tk.Toplevel):
  def __init__(self, parent=None, **kw):
    tk.Toplevel.__init__(self, parent, **kw)
    self.title('设置用户信息')
    self.parent = parent # 显式地保留父窗口
    # 第一行（两列）
    row1 = tk.Frame(self)
    row1.pack(fill="x")
    tk.Label(row1, text='姓名：', width=8).pack(side=tk.LEFT)
    self.name = tk.StringVar()
    tk.Entry(row1, textvariable=self.name, width=20).pack(side=tk.LEFT)
    # 第二行
    row2 = tk.Frame(self)
    row2.pack(fill="x", ipadx=1, ipady=1)
    tk.Label(row2, text='年龄：', width=8).pack(side=tk.LEFT)
    self.age = tk.IntVar()
    tk.Entry(row2, textvariable=self.age, width=20).pack(side=tk.LEFT)
    # 第三行
    row3 = tk.Frame(self)
    row3.pack(fill="x")
    tk.Button(row3, text="取消", command=self.cancel).pack(side=tk.RIGHT)
    tk.Button(row3, text="确定", command=self.ok).pack(side=tk.RIGHT)
  def ok(self):
    # 显式地更改父窗口参数
    self.parent.name = self.name.get()
    self.parent.age = self.age.get()
    # 显式地更新父窗口界面
    self.parent.l1.config(text=self.parent.name)
    self.parent.l2.config(text=self.parent.age)
    self.destroy() # 销毁窗口
  def cancel(self):
    self.destroy()
    
# 主窗
class MyApp(tk.Tk):
  
  def __init__(self, master=None, **kw):
    tk.Tk.__init__(self, master, **kw)
    # self.pack() # 若继承 tk.Frame，此句必须有！！！
    self.title('用户信息')
    # 程序参数
    self.name = '张三'
    self.age = 30
    # 程序界面
    self.setupUI()
    
  def setupUI(self):
    # 第一行（两列）
    row1 = tk.Frame(self)
    row1.pack(fill="x")
    tk.Label(row1, text='姓名：', width=8).pack(side=tk.LEFT)
    self.l1 = tk.Label(row1, text=self.name, width=20)
    self.l1.pack(side=tk.LEFT)
    # 第二行
    row2 = tk.Frame(self)
    row2.pack(fill="x")
    tk.Label(row2, text='年龄：', width=8).pack(side=tk.LEFT)
    self.l2 = tk.Label(row2, text=self.age, width=20)
    self.l2.pack(side=tk.LEFT)
    # 第三行
    row3 = tk.Frame(self)
    row3.pack(fill="x")
    tk.Button(row3, text="设置", command=self.setup_config).pack(side=tk.RIGHT)
    
  # 设置参数
  def setup_config(self):
    pw = PopupDialog(self)
    self.wait_window(pw) # 这一句很重要！！！
    return
  
if __name__ == '__main__':
  app = MyApp()
  app.mainloop()
