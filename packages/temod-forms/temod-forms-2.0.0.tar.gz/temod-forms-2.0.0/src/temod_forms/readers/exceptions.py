class TemodReaderException(Exception):
	"""docstring for TemodReaderException"""
	def __init__(self, code, *args, exception=None, **kwargs):
		super(TemodReaderException, self).__init__(*args, **kwargs)
		self.exception = exception
		self.code = code
		
	def __repr__(self):
		s = f"TemodReaderError (code = {self.code})"
		if self.exception is not None:
			s += f"{s}\n{self.exception}"
		return s
		
	def __str__(self):
		s = f"TemodReaderError (code = {self.code})"
		if self.exception is not None:
			return f"{s}\n{self.exception}"
		return s
		