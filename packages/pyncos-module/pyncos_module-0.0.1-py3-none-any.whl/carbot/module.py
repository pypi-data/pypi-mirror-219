#-*- coding:utf-8 -*- 

from abc import abstractmethod
import os
from uuid import uuid4


class ModuleBase:
  

  __slot_name__ = ''
  '''
    The name of slot which to register
  '''  

  __module_name__ = ''
  '''
    The name of current module
  '''
  
  @abstractmethod
  def connect(self):
    pass
  
  
  @abstractmethod
  def disconnect(self):
    pass
  
  
  @abstractmethod
  def install(self):
    pass
  
  
  @abstractmethod
  def start(self):
    pass
  
  
  def loop_start(self):
    self.start()
  
  
  @abstractmethod
  def stop(self):
    pass
  
  
  def loop_stop(self):
    self.stop()
    
    
  def run(self):
    if not self.connect():
      self.handle_error('Module {0} connect failed to host'.format(self.__module_name__))
      os._exit(-1)
    
    self.loop_start()
    
    self.loop_stop()
    
    self.disconnect()
    
  
  @abstractmethod
  def handle_error(self, error):
    pass
    
  def __id_genertor__(self, localfile) -> str:
    '''
    生成ID或从本地读取ID
    '''
    if not os.path.exists(localfile):
      os.makedirs(localfile)
    
    if os.path.exists(localfile):
      with open(localfile, 'r') as f:
        line = f.readline()
        print(line)
        if len(line) > 0 and ':' in line:
          slot, id = line.split(':')[:2:]
          return id
        
    with open(localfile, 'w') as f:
      id = str(uuid4()).replace('-', '')
      slot = self.__slot_name__
      line = '{0}:{1}'.format(slot, id)
      f.writelines([line])
      return id
    
    
  def __crc16__(self, buff:list):
    data = bytearray(buff)
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ 0x8408
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    
    # crc = (crc << 8) | ((crc >> 8) & 0xFF) # 小端模式放开注释
    
    return crc & 0xFFFF
    
    
  def __to_bytes__(self, val:int, byteorder='big'):
    '''
      自动转换成对应字节长度的bytes
    '''
    if val >= 0 and val <= 255 :
      return val.to_bytes(1, byteorder)
    
    if val > 255 and val <= 65535:
      return val.to_bytes(2, byteorder)
    
    if val > 65535 and val <= 4294967295:
      return val.to_bytes(4, byteorder)
    
    raise Exception('out of range when the __to_bytes__ invoke ')
   