from flask import request, abort

def body_content(content,*dargs,strict=False,on_error=None,objectifier=None,**dkwargs):

	if on_error is None:
		on_error = lambda :abort(415)
	if objectifier is None:
		objectifier = lambda x:x

	def __extractor(endpoint):
		def __verification(*args,**kwargs):
			data = None
			if content == "json":
				if request.json is None and strict:
					on_error()
				elif request.json is not None:
					data = request.json
			elif content == "form":
				if request.form is None and strict:
					on_error()
				elif request.form is not None:
					data = dict(request.form)
			return endpoint(objectifier(data,*args,**kwargs),*args,**kwargs)

		__verification.__name__ = endpoint.__name__
		return __verification

	return __extractor