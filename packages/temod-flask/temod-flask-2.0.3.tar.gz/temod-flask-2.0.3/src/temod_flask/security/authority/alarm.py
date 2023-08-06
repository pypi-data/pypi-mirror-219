from pythonjsonlogger import jsonlogger
from pprint import pprint

from .exceptions import *
from .utils import *

import logging.handlers as handlers
import logging


class Alarm(object):
	"""docstring for Alarm"""
	def __init__(self,name=""):
		super(Alarm, self).__init__()
		self.name = name

	def trigger(self,**data):
		print(f"Alarm {self.name} triggered: ")
		pprint(data)


class TimedRotatingJsonFileAlarm(Alarm):
	"""docstring for TimedRotatingJsonFileAlarm"""
	def __init__(self, filename, logger_name=None, when="D", interval=1, encoding="utf-8", backupCount=0, delay=True, 
		utc=False, atTime=None, errors=None, default_state='info', level=logging.WARNING):
		super(TimedRotatingJsonFileAlarm, self).__init__(name=filename)
		try_assert(
			default_state in ['debug','info','warning','error','critical'],MalformedAlarmError,
			"Alarm default state must be one of the following: debug, info, warning, error, critical"
		)

		self.default_state = default_state

		if logger_name is None:
			self.logger = logging.getLogger()
		else:
			self.logger = logging.getLogger(logger_name)
		self.logger.setLevel(level)

		logHandler = handlers.TimedRotatingFileHandler(
			self.name,when=when,interval=interval,encoding=encoding,backupCount=backupCount,delay=delay,
			utc=False,atTime=atTime,errors=errors
		)

		formatter = jsonlogger.JsonFormatter()
		logHandler.setFormatter(formatter)
		self.logger.addHandler(logHandler)

	def trigger(self,**data):
		level = self.default_state
		if data.get('level',None) in ['debug','info','warning','error','critical']:
			level = data.pop('level')
		getattr(self.logger,level)(data)