
def try_assert(condition,exception_type,*exc_args,**exc_kwargs):
	try:
		assert(condition)
	except AssertionError:
		raise exception_type(*exc_args,**exc_kwargs)