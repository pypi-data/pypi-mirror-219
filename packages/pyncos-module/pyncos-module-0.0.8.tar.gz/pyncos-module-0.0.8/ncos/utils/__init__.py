# -*- coding:utf-8 -*-
from ncos.utils.logger import Logger, TextWritter, ConsoleWritter
from ncos.commons import LOGS_ENABLE, LOGS_PATH
if LOGS_ENABLE:
  __logger__ = Logger(TextWritter(LOGS_PATH))
else:
   __logger__ = Logger(ConsoleWritter())

LOG_INFO          = __logger__.info
LOG_DEBUG         = __logger__.debug
LOG_ERROR         = __logger__.error
LOG_FETAL         = __logger__.fetal
