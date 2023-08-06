class MalformedAuthenticatorError(Exception):
	"""docstring for MalformedAuthenticatorError"""
	def __init__(self, *args, **kwargs):
		super(MalformedAuthenticatorError, self).__init__(*args, **kwargs)