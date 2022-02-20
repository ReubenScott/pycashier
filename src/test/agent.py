#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import re
import time
import codecs
import psycopg2


  
'''
 def on_find(): 
    t2 = Toplevel(root) 
    t2.title('Find') 
    t2.geometry('262x65+200+250') 

    t2.transient(root) 
    Label(t2, text="Find All:").grid(row=0, column=0, sticky='e') 
         v=StringVar() 
         e = Entry(t2, width=25, textvariable=v) 
    e.grid(row=0, column=1, padx=2, pady=2, sticky='we') 
    e.focus_set() 
    c=IntVar() 
    Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, 
    column=1, sticky='e', padx=2, pady=2) 
    Button(t2, text="Find All", underline=0,  command=lambda: 
    search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0, 
    column=2, sticky='e'+'w', padx=2, pady=2) 

 def close_search(): 
    textPad.tag_remove('match', '1.0', END) 
    t2.destroy() 

 t2.protocol('WM_DELETE_WINDOW', close_search)#override close 

'''




if __name__=="__main__":  
  # python /cdipgpfs/etl/bin/fileProcess.py 00000002 20180729
  # 系统代号 业务日期 数据文件 标识文件
  # 参数一 任务ID / 上游系统代码   '00000001'
  task_id = sys.argv[1]
  # 参数二 业务日期
  bus_date = sys.argv[2]

  #获取上游文件任务配置
  conn = psycopg2.connect(database="edwdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
  #conn = psycopg2.connect(database="template1", user="postgres", password="postgres", host="192.168.0.105", port="5432")
  cr = conn.cursor()
  sql = "select ruletype, rulecontent, ruledesc from CDIP_TASK_RULE_CONFIG where receiveid = %s "   
  
  cr.execute(sql, [task_id])
  rs = cr.fetchone()
  cr.close()
  

  #同时给多个变量赋值
  rule_type , rule_content, rule_description = rs
  
  #for rule_type , rule_content, rule_description in rs:
  print type(rs)
  print rule_type 
  print rule_content
  print rule_description  