class FormContent(object):
	"""docstring for FormContent"""
	def __init__(self, extracted, warnings=None, errors=None, data=None):
		super(FormContent, self).__init__()
		self.warnings = [] if warnings is None else warnings
		self.errors = [] if errors is None else errors
		self.data = {} if data is None else data
		self.extracted = extracted

	def getObject(self):
		return self.extracted

	def getErrors(self,url_formatted=False):
		print(self.errors)
		if url_formatted:
			return ("errors="+";".join([self.errorRepr(error) for error in self.errors])) if len(self.errors) > 0 else ""
		return self.errors

	def getWarnings(self,url_formatted=False):
		if url_formatted:
			return ("warnings="+";".join([self.errorRepr(warning) for warning in self.warnings])) if len(self.warnings) > 0 else ""
		return self.warnings

	def errorRepr(self,error):
		return f"{error.exception.attribute.name}${error.code}" if getattr(error,"exception",None) is not None else f"{error.code}"

	def urlQuery(self):
		errors = self.getErrors(url_formatted=True)
		warnings =  self.getWarnings(url_formatted=True)
		a = "&" if len(errors) > 0 or len(warnings) > 0 else ""
		b = "&" if len(errors) > 0 and len(warnings) > 0 else ""
		values = "&".join([f"{k}={v}" for k,v in self.data.items()])
		return f"{errors}{a}{warnings}{b}{values}"

