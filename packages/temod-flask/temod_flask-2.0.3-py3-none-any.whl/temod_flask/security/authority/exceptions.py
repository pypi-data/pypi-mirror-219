class MalformedLawBookError(Exception):
	"""docstring for MalformedLawBookError"""
	def __init__(self, *args, **kwargs):
		super(MalformedLawBookError, self).__init__(*args, **kwargs)

class ImmutableLawBookError(Exception):
	"""docstring for ImmutableLawBookError"""
	def __init__(self, *args, **kwargs):
		super(ImmutableLawBookError, self).__init__(*args, **kwargs)

class MalformedGardianError(Exception):
	"""docstring for MalformedGardianError"""
	def __init__(self, *args, **kwargs):
		super(MalformedGardianError, self).__init__(*args, **kwargs)

class LockException(Exception):
	"""docstring for LockException"""
	def __init__(self, *args, **kwargs):
		super(LockException, self).__init__(*args, **kwargs)

class MalformedAlarmError(Exception):
	"""docstring for MalformedAlarmError"""
	def __init__(self, *args, **kwargs):
		super(MalformedAlarmError, self).__init__(*args, **kwargs)
		