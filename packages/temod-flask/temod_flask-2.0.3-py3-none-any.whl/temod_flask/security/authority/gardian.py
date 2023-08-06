from .exceptions import *
from .alarm import Alarm
from .right import *
from .utils import *

from datetime import datetime


class Gardian(object):
	"""docstring for Gardian"""
	def __init__(self, decision_function=lambda:True, alarm=None,strict=False):
		super(Gardian, self).__init__()
		if alarm is not None:
			try_assert(
				issubclass(type(alarm),Alarm),MalformedGardianError,"Gardian's alarm must be a subclass of Alarm."
			)
		else:
			print(f"Warning: The gardian has no alarm to trigger in case of unwanted actions.")
		self.decision_function = decision_function
		self.post_alarms = {"default":lambda:None}
		self.security_gates = {}
		self.strict = strict
		self.alarm = alarm

	def add_security_gate(self,function_,gate_id=None):
		id_ = gate_id if gate_id is not None else function_.__name__
		if id_ in self.security_gates:
			if self.strict:
				raise DuplicatedLockError(f"A function with name '{id_}' is already beeing locked by the gardian.")
			print(f"Warning: A function with name '{id_}' is already beeing locked by the gardian.")
		self.security_gates[id_]=function_
		return id_

	def decision(self,f):
		self.decision_function = f

	def alarm_response(self,*levels):
		try_assert(
			all([level in ['default','debug','info','warning','error','critical'] for level in levels]),MalformedGardianError,
			"Alarm level must be one of the following: default, debug, info, warning, error, critical"
		)
		def __response(f):
			for level in levels:
				self.post_alarms[level] = f
		return __response

	def lock_function(self, *dargs, lock_name=None, alarm_snapshot=None, trigger_alarm=True, post_alarm=None, endpoint_kwargs=None, **dkwargs):

		def __lock(locked_function):
			id_ = self.add_security_gate(locked_function,gate_id=lock_name)

			def __verification(*args,**kwargs):
				extras = {} if endpoint_kwargs is None else {k:kwargs.get(k,None) for k in endpoint_kwargs}
				decision = self.decision_function(*dargs,**dkwargs,**extras)
				if type(decision) is bool:
					if decision:
						return locked_function(*args,**{k:v for k,v in kwargs.items() if not k in extras})
				elif type(decision) is dict:
					return locked_function(*args,**{k:v for k,v in kwargs.items() if not k in extras},**decision)

				alert_level = 'default'
				if trigger_alarm and self.alarm is not None:
					data = {"at_function":id_,"time":datetime.now()}
					if alarm_snapshot is not None:
						data.update(alarm_snapshot())
					alert_level = data.get('level','default')
					self.alarm.trigger(**data)
				if post_alarm is not None:
					return post_alarm()
				return self.post_alarms.get(alert_level,'default')()

			__verification.__name__ = id_
			return __verification

		return __lock



class LawBookGardian(Gardian):
	"""docstring for LawBookGardian"""

	DEFAULT_USER_LOADER = None

	def __init__(self, lawBook, userRightsReader, index=None, **kwargs):
		super(LawBookGardian, self).__init__(
			decision_function= lambda x,y,**z: self.has_rights(x(),y,**z) ,
			**kwargs
		)

		try_assert(
			issubclass(type(lawBook),LawBook),MalformedGardianError,"LawBookGardian's law book must be a subclass of LawBook."
		)
		try_assert(
			hasattr(userRightsReader,"__call__"),MalformedGardianError,"LawBookGardian's verification process must be a callable object."
		)
		try_assert(
			hasattr(index,"__call__"),MalformedGardianError,"LawBookGardian's rights index must be a callable object."
		)

		if index is not None:
			try_assert(
				hasattr(index,"__call__"),MalformedGardianError,"LawBookGardian's rights index must be a callable object."
			)
			try_assert(
				len(set([index(right) for right in lawBook.list_rights()])) == len(lawBook.rights),MalformedGardianError,
				"LawBookGardian's rights index must keep the unicity of every right in the law book."
			)

		self.userRightsReader = userRightsReader
		self.lawBook = lawBook
		self.index = index

	def rights(self):
		return self.lawBook.list_rights()
			
	def has_right(self,user,right):
		if self.index is None:
			idx = right
		else:
			idx = self.index(self.lawBook.rights[right])
		return idx in self.userRightsReader(user)

	def has_rights(self, user, rights, mode="any"):
		if mode == 'any' and any([self.has_right(user,right) for right in rights]):
			return True
		if mode == "all" and all([self.has_right(user,right) for right in rights]):
			return True
		return False

	def lock_function(self,rights, user_loader=None, mode='any',**kwargs):

		if user_loader is None:
			user_loader = lambda: LawBookGardian.DEFAULT_USER_LOADER()

		return super(LawBookGardian,self).lock_function(
			user_loader,rights,mode=mode,**kwargs
		)

		