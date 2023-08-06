class JoinException(Exception):
	"""docstring for JoinException"""
	def __init__(self, *args, **kwargs):
		super(JoinException, self).__init__(*args, **kwargs)

class JoinStorageException(Exception):
	"""docstring for JoinStorageException"""
	def __init__(self, *args, **kwargs):
		super(JoinStorageException, self).__init__(*args, **kwargs)

class JoinQueryingException(Exception):
	"""docstring for JoinQueryingException"""
	def __init__(self, *args, **kwargs):
		super(JoinQueryingException, self).__init__(*args, **kwargs)
