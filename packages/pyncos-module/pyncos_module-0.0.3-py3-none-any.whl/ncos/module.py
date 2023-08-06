#-*- coding:utf-8 -*- 

from abc import abstractmethod
import os
from uuid import uuid4
from networks.mqtt import MqttClient
from json import dumps, loads
from utils import LOG_DEBUG, LOG_ERROR
from commons import *

class ModuleBase:
  

  __slot_name__ = ''
  '''
    The name of slot which to register
  '''  

  __module_name__ = ''
  '''
    The name of current module
  '''
  
  def __init__(self):
    self.broker = None
    self.id = self.__id_genertor__(DATA_ROOT_PATH, DATA_LOCAL_FILE)
    self.installed = False
    self.subscriptions = {
      
      self.__topic__(NCOS_READY_TOPIC):                     self.on_NCOS_ready,
      self.__topic__(MODULES_INSTALL_PUSH_TOPIC):           self.on_installed,
      self.__topic__(MODULES_DATA_PULL_TOPIC):              self.on_data_pull,
      self.__topic__(MODULES_CONFIG_TOPIC):                 self.on_config,
      self.__topic__(MODULES_ACTION_TOPIC):                 self.on_action
    }

  
  def install(self):
    self.handle_post_install()
    self.broker.publish(
      'NCOS/modules/install', 
      dumps({'slot': self.__slot_name__, 'moduleId': self.id, 'moduleName': self.__module_name__}))

  def on_installed(self, topic, payload:dict):
    _success = payload['success'] if 'success' in payload else False
    _error = payload['error'] if 'error' in payload else ''
    self.handle_installed(_success, _error)
    
    
  def on_NCOS_ready(self, topic, payload:dict):
    self.handle_NCOS_ready(payload)
  
  
  def on_data_pull(self, topic, payload:dict):
    self.handle_data_pull(payload)
  
  
  def on_config(self, topic, payload:dict):
    self.handle_config(payload)
  
  
  def on_action(self, topic, payload:dict):
    self.handle_action(payload)

  

  def loop_start(self):
    self.handle_connect()
    self.handle_startup()
    self.broker.loop()
    
  
  def loop_stop(self):
    self.handle_disconnect()
    self.handle_exit()
    
    
  def add_topic(self, topic:str, accessor:function):
    self.subscriptions.update({topic: accessor})
      
    
  def bind_ncos_broker(self, host:str, port:int):
    self.broker = MqttClient(host, port)
    
    def on_connected(client, userdata, flags, rc):
      
      for topic in self.subscriptions:
        self.broker.subscribe(topic)
      self.handle_broker_connected(client, userdata, flags, rc)
      
    def on_messaged(client, userdata, msg):
      LOG_DEBUG('[Broker] {0} {1}'.format(msg.topic, str(msg.payload, encoding='utf-8')))
      topic = msg.topic
      payload = loads(str(msg.payload, encoding='utf-8'))
      
      if topic in self.subscriptions:
        self.subscriptions[topic](topic, payload)
      
    self.broker.attach_connected(on_connected)
    self.broker.attach_messaged(on_messaged)
    self.broker.connect()
    
    
  def set_will(self, content:str):
    self.mqtt.set_will('NCOS/modules/{0}/uninstall'.format(self.id), dumps({'moduleId': self.id, 'reason': content}))

  
  def run(self):
    
    self.loop_start()
    self.loop_stop()


  @abstractmethod
  def handle_connect(self):
    pass
  
  
  @abstractmethod
  def handle_disconnect(self):
    pass
  
  
  @abstractmethod
  def handle_startup(self):
    pass
  
  
  @abstractmethod
  def handle_exit(self):
    pass

  @abstractmethod
  def handle_post_install(self):
    pass
  
  
  @abstractmethod
  def handle_broker_connected(self, client, userdata, flags, rc):
    pass
  
  
  @abstractmethod
  def handle_NCOS_ready(self, data):
    pass
  
  
  @abstractmethod
  def handle_data_pull(self, data):
    pass
  
  
  @abstractmethod
  def handle_config(self, data):
    pass
  
  
  @abstractmethod
  def handle_action(self, data):
    pass
  
  
  @abstractmethod
  def handle_installed(self, result:bool, reason:str):
    pass
  
      
  @abstractmethod
  def handle_error(self, error):
    pass
      
  
  def __topic__(self, topic):
    return topic.replace('${moduleId}', self.id).replace('${slotName}', self.__slot_name__)

    
  def __id_genertor__(self, local_dir, file_name) -> str:
    '''
    生成ID或从本地读取ID
    '''
    if not os.path.exists(local_dir):
      os.makedirs(local_dir)
      
    localfile = os.path.join(local_dir, file_name)
    
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
   