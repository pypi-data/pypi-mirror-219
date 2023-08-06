from . import Decorator
from ..base import *


class Bootstrap_4_0(object):
	"""docstring for Bootstrap_4_0"""
	def __init__(self):
		super(Bootstrap_4_0, self).__init__()

	def decorate(self,tag, propagate=True, required_inputs=None):
		required_inputs = [] if required_inputs is None else required_inputs
		if issubclass(type(tag), Table):
			tag.addClass("table")
		elif issubclass(type(tag),Form):
			if len(required_inputs) > 0:
				tag.addClass('needs-validation')
		elif issubclass(type(tag), Input):
			tag.addClass("form-control")
			if hasattr(tag,'name') and tag.name in required_inputs:
				tag.addAttribute("required","true")
		elif issubclass(type(tag), Button):
			tag.addClass("btn")
			if getattr(tag, "type", "button") == "submit":
				tag.addClass("btn-success")
		if propagate:
			for child in tag.children:
				self.decorate(child,required_inputs=required_inputs)
		return tag

class Bootstrap(Decorator):
	"""docstring for Bootstrap"""
	def __init__(self, version="4.0", **kwargs):
		super(Bootstrap, self).__init__()
		self.version = BOOTSTRAP_VERSIONS[version](**kwargs)

	def decorate(self,*args,**kwargs):
		return self.version.decorate(*args,**kwargs)


BOOTSTRAP_VERSIONS = {
	"4.0":Bootstrap_4_0
}


