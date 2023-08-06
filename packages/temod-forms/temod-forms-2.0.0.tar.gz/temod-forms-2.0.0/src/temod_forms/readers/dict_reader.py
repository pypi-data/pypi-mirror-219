from .exceptions import TemodReaderException
from .content import FormContent
from .utils import AdaptativeTimeParser

from datetime import datetime


class EntityDictReader(object):
	"""docstring for EntityDictReader"""
	def __init__(self, entity_type):
		super(EntityDictReader, self).__init__()
		self.entity_type = entity_type
		self.required = [attr['name'] for attr in self.entity_type.ATTRIBUTES if attr.get('required',False)]

	def autocomplete(self,data,to_complete,storage=None,date_readers=None):
		date_readers = {} if date_readers is None else date_readers
		if storage is None:
			if not hasattr(self.entity_type,"storage"):
				raise Exception("Entity storage must be specified in order to use the default autocomplete")
			storage = self.entity_type.storage
		for field,format_ in date_readers.items():
			if hasattr(format_,"__call__"):
				data[field] = format_(data[field])
			else:
				data[field] = datetime.strptime(data[field],format_)
		for attribute in to_complete:
			data[attribute] = storage.generate_value(attribute)

	def read(self,data,strict=True,storage=None,date_formats=None,date_fields=None,**kwargs):
		unspecified_required = [attr for attr in self.required if not attr in data]

		date_fields = [] if date_fields is None else date_fields
		date_readers = {date_field:AdaptativeTimeParser.parse_str for date_field in date_fields}
		date_readers.update({} if date_formats is None else date_formats)

		object_ = None; errors = []; original = {k:v for k,v in data.items()}
		try:
			if not strict and len(unspecified_required) > 0:
				self.autocomplete(data,unspecified_required,storage=storage,date_readers=date_readers)
			object_ = self.entity_type(**data)
		except Exception as exc:
			errors.append(TemodReaderException( str(getattr(exc,"code",getattr(exc,"CODE",type(exc).__name__))), exception=exc ))
		return FormContent(object_,errors=errors,data=original)


class JoinDictReader(object):
	"""docstring for JoinDictReader"""
	def __init__(self, join_type):
		super(JoinDictReader, self).__init__()
		self.join_type = join_type
		self.entities_list = [join_type.STRUCTURE[0]]
		for rel in join_type.STRUCTURE[1:]:
			continue
			self.entities_list.append(rel[0])


	def read(self,data):
		return self.join_type(*[
			entity(**data.get(getattr(entity,"ENTITY_NAME",entity.__name__),{})) 
			for entity in self.entities_list
		])


class ClusterDictReader(object):
	"""docstring for ClusterDictReader"""
	def __init__(self, cluster_type):
		super(ClusterDictReader, self).__init__()
		self.cluster_type = cluster_type

	def read(self,data):
		pass
