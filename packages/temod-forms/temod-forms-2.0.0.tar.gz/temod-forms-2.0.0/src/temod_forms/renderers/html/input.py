from temod.base.attribute import *
from .base import *



class AttributeInput(Input):
	"""docstring for Input"""
	def __init__(self, attribute, **kwargs):
		super(Input, self).__init__("input", **kwargs)
		self.attribute = attribute

	def forAttribute(attr,**kwargs):
		if type(attr) is IntegerAttribute:
			return IntegerAttributeInput(attr,**kwargs)
		elif type(attr) is StringAttribute:
			if getattr(attr,'max_length',101) > 100:
				return TextAttributeInput(attr,**kwargs)
			return StringAttributeInput(attr,**kwargs)
		elif type(attr) is RealAttribute:
			return RealAttributeInput(attr,**kwargs)
		elif type(attr) is DateAttribute:
			return DateAttributeInput(attr,**kwargs)
		elif type(attr) is DateTimeAttribute:
			return DatetimeAttributeInput(attr,**kwargs)
		elif type(attr) is BooleanAttribute:
			return BooleanAttributeInput(attr,**kwargs)
		elif type(attr) is UTF8BASE64Attribute:
			return StringAttributeInput(attr,**kwargs)
		elif type(attr) is UUID4Attribute:
			return StringAttributeInput(attr,**kwargs)
		elif type(attr) is RangeAttribute:
			return RangeAttributeInput(attr,**kwargs)
		raise Exception(f"Type of attribute {type(attr)} is not handled yet")



class IntegerAttributeInput(NumericInput):
	"""docstring for IntegerAttributeInput"""
	def __init__(self, attribute, **kwargs):
		super(IntegerAttributeInput, self).__init__(
			step=1,
			min=getattr(attribute,"min_value",None),
			max=getattr(attribute,"max_value",None), 
			value=getattr(attribute,"value",getattr(attribute,"default_value",None)), 
			name=attribute.name,
			placeholder=getattr(attribute,"placeholder",attribute.name.replace('_',' ').title()),
			**kwargs
		)



class StringAttributeInput(TextInput):
	"""docstring for StringAttributeInput"""
	def __init__(self, attribute, **kwargs):
		super(StringAttributeInput, self).__init__(
			min=getattr(attribute,"min_length",None), 
			max=getattr(attribute,"max_length",None), 
			value=getattr(attribute,"value",getattr(attribute,"default_value",None)), 
			name=attribute.name,
			placeholder=getattr(attribute,"placeholder",attribute.name.replace('_',' ').title()),
			**kwargs
		)



class TextAttributeInput(TextAreaInput):
	"""docstring for TextAttributeInput"""
	def __init__(self, attribute, **kwargs):
		super(TextAttributeInput, self).__init__(
			min=getattr(attribute,"min_length",None), 
			max=getattr(attribute,"max_length",None), 
			value=getattr(attribute,"value",getattr(attribute,"default_value",None)), 
			name=attribute.name,
			placeholder=getattr(attribute,"placeholder",attribute.name.replace('_',' ').title()),
			**kwargs
		)



class RealAttributeInput(NumericInput):
	"""docstring for RealAttributeInput"""
	def __init__(self, attribute, **kwargs):
		super(RealAttributeInput, self).__init__(
			step=getattr(attribute,"precision",0.01),
			min=getattr(attribute,"min_value",None),
			max=getattr(attribute,"max_value",None), 
			value=getattr(attribute,"value",getattr(attribute,"default_value",None)), 
			name=attribute.name,
			placeholder=getattr(attribute,"placeholder",attribute.name.replace('_',' ').title()),
			**kwargs
		)



class DateAttributeInput(DateInput):
	"""docstring for DateAttributeInput"""
	def __init__(self, attribute, **kwargs):
		super(DateAttributeInput, self).__init__(
			value=getattr(attribute,"value",getattr(attribute,"default_value",None)), 
			name=attribute.name,
			placeholder=getattr(attribute,"placeholder",attribute.name.replace('_',' ').title()),
			**kwargs
		)



class DatetimeAttributeInput(DateTimeInput):
	"""docstring for DatetimeAttributeInput"""
	def __init__(self, attribute, **kwargs):
		super(DatetimeAttributeInput, self).__init__(
			value=getattr(attribute,"value",getattr(attribute,"default_value",None)), 
			name=attribute.name,
			placeholder=getattr(attribute,"placeholder",attribute.name.replace('_',' ').title()),
			**kwargs
		)



class BooleanAttributeInput(Select):
	"""docstring for BooleanAttributeInput"""
	def __init__(self, attribute, **kwargs):
		super(BooleanAttributeInput, self).__init__(
			[0,"False"],[1,"True"], 
			name=attribute.name,
			placeholder=getattr(attribute,"placeholder",attribute.name.replace('_',' ').title()),
			**kwargs
		)



class RangeAttributeInput(Select):
	"""docstring for RangeAttributeInput"""
	def __init__(self, attribute, options=None, **kwargs):
		options = {} if options is None else options
		values = {k:options.get(k,attribute.values[k]) for k in attribute.values}
		super(RangeAttributeInput, self).__init__(
			*values.items(), 
			name=attribute.name,
			placeholder=getattr(attribute,"placeholder",attribute.name.replace('_',' ').title()),
			**kwargs
		)

		
