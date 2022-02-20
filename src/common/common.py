#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import sys
import codecs
import logging
import platform


class Logger():
  
  def __init__(self, logname='xtwh.log', loglevel=logging.INFO, logger=''):
    self.loglevel = loglevel
    self.logger =  logger
    self.logger.setLevel(self.loglevel)
    
    #设置日志输出格式
    self.formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
    
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(self.loglevel)
    consoleHandler.setFormatter(self.formatter)    
    self.logger.addHandler(consoleHandler)
    
    self.fileHander = logging.FileHandler(logname)
    self.fileHander.setLevel(self.loglevel)
    self.fileHander.setFormatter(self.formatter)    
    self.logger.addHandler(self.fileHander)
    
  def getlog(self):
    return self.logger
  
  def setlogname(self, logname):
    self.logger.removeHandler(self.fileHander)
    
    self.fileHander = logging.FileHandler(logname)
    self.fileHander.setLevel(self.loglevel)
    self.fileHander.setFormatter(self.formatter)    
    self.logger.addHandler(self.fileHander)
  
  
def get_func_name():
  ''' 获取当前运行的函数名 '''
  return sys._getframe(1).f_code.co_name


def check_args_num(num):
  '''
     函数说明： 装饰器 检查函数参数数量
     Args:
       num: args 的数量
  
  '''
  def deco(func):
    def wrapper(*args, **kw):
      if len(args) != num:
        msg = "E|%参数个数有无，正确个数应为%s|%s|||" % (func.__name__, num, func.__name__)
        reurn msg
        
      return func(*args, **kw)
      
    return wrapper
  return deco




def set_env():
  
  global_var.OS = platform.system()
  
  
  
if __name__ == "__main__":
  set_env()
  
