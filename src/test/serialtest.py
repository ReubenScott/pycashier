#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import serial
import MySQLdb

ser = serial.Serial('COM5',9600)


#获取一行信息
def recv(serial):
    data = ''
    while serial.inWaiting() > 0:
        data += serial.read(1)
   
    return data


def GetInfo(db,data):
    data = data[0:-1]  #最后面有一个空格，需要去掉，否则会影响读数据库
    print data
    ret = 0.0 
    try:
        cur = db.cursor()
        sql="set names utf8"    #这一条语句是告诉数据库编码方式为 utf8
        cur.execute(sql)

        sql = "select * from productinfo where code=%s"%(data)
        #print sql
        cur.execute(sql)
        #sql = "select * from productinfo where(code=%s)"
        #cur.execute(sql,data)       
        results = cur.fetchall()
        #print results
        for row in results:
            code = row[0]
            #print code
            price = row[1]
            #print price
            info = row[2]
            #print info
            ret = price
               #解析出来的信息可能为中文，直接print肯定是不行的，需要转化为windows下的GBK编码
            print 'coding=',row[0],'price=',row[1],'info=',info.decode('UTF-8').encode('GBK')              
    except:
        print 'it has no infomation about %s'%(data)

    return ret


db = MySQLdb.connect('localhost','root','',"zou",3306,'utf8')
cursor = db.cursor()

#cursor.execute("DROP TABLE IF EXISTS productinfo")

'''
sql="""CREATE TABLE productinfo(
        code  CHAR(18),
        price double(9,2),
        info  CHAR(25))"""
cursor.execute(sql)
'''    
        
sum = 0.0          
while True:
    data = recv(ser)
    if data != '':
        #print data
        sum += GetInfo(db,data)
        print '总付款:',sum
         

db.close()
ser.close()              
