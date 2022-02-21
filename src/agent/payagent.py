#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import sys 
import socket
import uuid
import traceback
import logging
import logging.config
 
logger = logging.getLogger(__name__)
 
# load config from file 
# logging.config.fileConfig('logging.ini', disable_existing_loggers=False) 
# or, for dictConfig
 
logging.config.dictConfig({
  'version': 1,              
  'disable_existing_loggers': False,  # this fixes the problem

  'formatters': {
    'standard': {
      'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    },
  },
  
  'handlers': {
    'console': {
      'level':'INFO',    
      'class':'logging.StreamHandler',
      'formatter': 'standard',
    },  
  },
  
  'loggers': {
    'console': {                  
      'handlers': ['console'],        
      'level': 'INFO',  
      'propagate': True  
    }
  },
 
  "root": {
    "level": "INFO",
    "handlers": ["console"]
  }

})

 
logger.info('It works!')

server_ip = 'localhost'
#server_ip = '192.168.1.2'


def search_goods_by_code(code):
  try:
    # 获取主机名
    hostname = socket.gethostname()
    #获取IP
    ip = socket.gethostbyname(hostname)
    # 获取Mac地址
    def get_mac_address():
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0,11,2)])
    
    # ipList = socket.gethostbyname_ex(hostname)
    # print(ipList)
    print("hostname ：",hostname)
    print("IP ：",ip)
    print("Mac ：",get_mac_address())
    
    test_data = {'host':hostname,'ip':ip,'mac':get_mac_address()}
    #requrl = 'http://127.0.0.1:12345/wm/1?u=12'   000000011  6901121300298
    #requrl = 'http://127.0.0.1:12345/se/1?u=' + code
    #requrl = 'http://localhost:8080/demo/cashier/findGoods.htm?barcode=' + code 
    requrl = 'http://'+ server_ip + ':8080/cashier/findGoods.htm?barcode=' + code 
    #req = requests.post(url = requrl,data =test_data_urlencode)
    response = requests.post(url=requrl, json=json.dumps(test_data))
#     response=requests.post(url=url,headers=headers,data=data_search)
    if response.status_code==200:
      print(response.json())
    else:
      print(response.status_code)
    res_data = req.json()
    res = res_data.read()
    print("addArticleFromSpider():" , res)
    print(type(res) )
    if res != None and res.strip() != '':
      #hjson = json.loads(res).encode('utf-8')
      #hjson = json.loads(hjson)
      hjson = json.loads(res)
      print(hjson)
      print(type(hjson))
      print(type(hjson['success']) , hjson['success'])
      if hjson['success'] == True :
        goods =  hjson['data']
        print(type(goods))
     # return tuple(eval(res))
        return goods
      else:
        print(hjson['msg'])
        return 
      
    else:
      return None
  except:
    traceback.print_exc()
    print(traceback.format_exc())
#     pass


# 预支付接口 返回 Token 
def prePayment():
  try:
    # 获取主机名
    hostname = socket.gethostname()
    #获取IP
    ip = socket.gethostbyname(hostname)
    # 获取Mac地址
    def get_mac_address():
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0,11,2)])
    
    # ipList = socket.gethostbyname_ex(hostname)
    # print(ipList)
    print("hostname ：",hostname)
    print("IP ：",ip)
    print("Mac ：",get_mac_address())
    
    test_data = {'host':hostname,'ip':ip,'mac':get_mac_address()}
    test_data_urlencode = urllib.urlencode(test_data)
    
    #requrl = 'http://localhost:8080/demo/cashier/prePayment.htm'
    requrl = 'http://'+ server_ip + ':8080/cashier/cashier/prePayment.htm' 
    req = requests.post(url=requrl, data=test_data_urlencode)
#     res_data = urllib2.post(req)
    res = res_data.read()
    print("addArticleFromSpider():" , res)
    print(type(res) )
    if res != None and res.strip() != '':
      #hjson = json.loads(res).encode('utf-8')
      #hjson = json.loads(hjson)
      hjson = json.loads(res)
      print(hjson)
      print(type(hjson))
      print(type(hjson['success']) , hjson['success'])
      if hjson['success'] == True :
        token =  hjson['data']
        # 商品编号 商品名称 单位 规格 零售价 会员价 折扣
        return token 
     # return tuple(eval(res))
      else:
        print(hjson['msg'])
    return     
  except:
    traceback.print_exc()
    print(traceback.format_exc())
#     pass
  
  
    
# 支付接口  Token 
def payment(token):
  try:
    # 获取主机名
    hostname = socket.gethostname()
    #获取IP
    ip = socket.gethostbyname(hostname)
    # 获取Mac地址
    def get_mac_address():
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0,11,2)])
    
    # ipList = socket.gethostbyname_ex(hostname)
    # print(ipList)
    print("hostname ：",hostname)
    print("IP ：",ip)
    print("Mac ：",get_mac_address())
    
    test_data = {'host':hostname,'ip':ip,'mac':get_mac_address(),'token':token}
    test_data_urlencode = urllib.urlencode(test_data)
    
    #requrl = 'http://localhost:8080/demo/cashier/payment.htm' 
    requrl = 'http://'+ server_ip + ':8080/cashier/cashier/payment.htm' 
    
    req = requests.post(url=requrl, data=test_data_urlencode)
#     res_data = urllib2.post(req)
    res = res_data.read()
    print("addArticleFromSpider():" , res)
    print(type(res) )
    if res != None and res.strip() != '':
      #hjson = json.loads(res).encode('utf-8')
      #hjson = json.loads(hjson)
      hjson = json.loads(res)
      print(hjson)
      print(type(hjson))
      print(type(hjson['success']) , hjson['success'])
      if hjson['success'] == True :
        token =  hjson['data']
        # 商品编号 商品名称 单位 规格 零售价 会员价 折扣
        return token 
     # return tuple(eval(res))
      else:
        print(hjson['msg'])
    return     
  except:
    traceback.print_exc()
    print(traceback.format_exc())
#     pass
  