# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import os
from datetime import datetime

class LogWritter(metaclass = ABCMeta):
  
  @abstractmethod
  def write(self, text):
    pass
  

class TextWritter(LogWritter):
  
  def __init__(self, path):
    self.path = path
    self.filefmt = '%Y_%m_%d.log'
    if not os.path.exists(self.path):
      os.makedirs(self.path)
      
    self.file = os.path.join(self.path, datetime.now().strftime(self.filefmt))
    
  def write(self, text):
    try:
      print(text)
      with open(self.file, 'a') as f:
        f.write(text + '\n')
    except:
      pass


class ConsoleWritter(LogWritter):
  
  def __init__(self):
    pass
  
  
  def write(self, text):
    print(text)


class Logger:
  
  @staticmethod
  def create(writter):
    return Logger(writter)  
  
  
  def __init__(self, writter): 
    self.writter = writter
    self.timefmt = '%H:%M:%S.%f'
  
  
  def log(self, level, text):
    self.writter.write('{0} - [{1}] {2}'.format(datetime.now().strftime(self.timefmt), level, text))
  
  
  def debug(self, text):
    self.log('debug', text)
    
    
  def info(self, text):
    self.log('info', text)
  
  
  def warn(self, text):
    self.log('warn', text)
    

  def error(self, text):
    self.log('error', text)
    
    
  def fetal(self, text):
    self.log('fetal', text)
    