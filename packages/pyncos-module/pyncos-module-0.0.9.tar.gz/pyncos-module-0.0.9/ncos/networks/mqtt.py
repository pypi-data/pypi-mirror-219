# -*- coding:utf-8 -*-

from paho.mqtt import client as mqtt_client
from uuid import uuid4

from ncos.utils import LOG_DEBUG


class MqttClient:
  
  
  def __on_messaged__(self, client, userdata, msg):
    if self.on_messaged:
      self.on_messaged(self, userdata, msg)

  def __on_connected__(self, client, userdata, flags, rc):
    LOG_DEBUG("Broker connected to {0},{1}".format(self.host, self.port))
    if self.on_connected:
      self.on_connected(self, userdata, flags, rc)
  
  def __init__(self, host:str, port:int = 1883):
    self.host = host
    self.port = port
    self.clientId = str(uuid4())
    self.on_connected = None
    self.on_messaged = None
    
    self.client = mqtt_client.Client(self.clientId)
    self.client.on_message = self.__on_messaged__
    self.client.on_connect = self.__on_connected__
    
    
  def set_will(self, topic, payload):
    self.client.will_set(topic, payload)
    
  
  def attach_messaged(self, onMessaged):
    self.on_messaged = onMessaged
  
  
  def attach_connected(self, onConnected):
    self.on_connected = onConnected
  
  
  def connect(self):
    self.client.connect(self.host, self.port)
    
  
  def subscribe(self, topic:str, qos = 0):
      self.client.subscribe(topic, qos)
  
  
  def subscribes(self, topics:tuple|list, qos = 0):
    for t in topics:
      self.client.subscribe(t, qos)
  
  
  def publish(self, topic, payload, qos = 0):
    self.client.publish(topic, payload, qos)
  
  
  def loop(self):
    try:
      self.client.loop_forever()
    except KeyboardInterrupt:
      return
    
    
  