#-*- coding:utf-8 -*-
import os


# Broker Subscriptions
NCOS_READY_TOPIC                      = 'NCOS/dev/ready'
MODULES_INSTALL_PUSH_TOPIC            = 'NCOS/dev/modules/${moduleId}/install/push'
MODULES_DATA_PULL_TOPIC               = 'NCOS/dev/slots/${slotName}/data/pull'
MODULES_CONFIG_TOPIC                  = 'NCOS/dev/slots/${slotName}/${moduleId}/config'
MODULES_ACTION_TOPIC                  = 'NCOS/dev/slots/${slotName}/action'

#
LOGS_ENABLE                           = False
LOGS_PATH                             = os.path.join('.','logs')

#DATA DUMPS
DATA_ROOT_PATH                        = os.path.join('.', 'data')
DATA_LOCAL_FILE                       = 'local'