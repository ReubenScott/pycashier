#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import Tkinter as tk
import time


def processButton():  
  '''
  t2 = tk.Toplevel(window) 
  t2.title('Find') 
  t2.geometry('262x65+200+250') 
  t2.transient(window) 
  '''
  if v1.get() == 1:
      #print text.get("0.0", "end")
     # t= text.get("0.0", "2.0")
      #print t
      window2 = tk.Tk()  # 创建一个窗口
      window2.title("result")  # 设置标题
      text2 = tk.Text(window2)
      text2.pack()
      text2.insert('end','T1\n')

      text2.insert('end', 'R1')
      #text2.insert('end',t)
  else:
      t=text.get("0.0", "end")
      window2 = tk.Tk()  # 创建一个窗口
      window2.title("result")  # 设置标题
      text2 = tk.Text(window2)
      text2.pack()
      #time.sleep(15)
      text2.insert('end', 'T1'+'\nR2'+'\nT2'+'\nR2')
      
        
        
window = tk.Tk()  # 创建一个窗口
window.title("Demo 2")  # 设置标题

frame1 = tk.Frame(window)  # 创建一个框架
frame1.pack()  # 将框架frame1放置在window中

# 
text = tk.Text(window)
text.pack()

v1 = tk.IntVar()

rbDanju = tk.Radiobutton(frame1, text="单句分析", variable=v1, value=1, )
rbPiliang =tk.Radiobutton(frame1, text="批量分析", variable=v1, value=2, )
rbFenxi = tk.Button(frame1, text="分析", command = processButton)

# grid布局
rbDanju.grid(row=1, column=1)
rbPiliang.grid(row=1, column=2)
rbFenxi.grid(row=1,column=3)


frame2 =tk.Frame(window)  # 创建框架frame2
frame2.pack()  # 将frame2放置在window中

# 创建消息
l1=tk.Label(frame2, text="单句分析只分析文本第一行",justify='left')

# grid布局
l1.grid(sticky=tk.E)

# 监测事件直到window被关闭
window.mainloop()