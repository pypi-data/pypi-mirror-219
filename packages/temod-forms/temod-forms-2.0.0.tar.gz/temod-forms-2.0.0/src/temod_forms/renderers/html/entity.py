from temod.base.entity import Entity
from .input import *
from .base import *


ENTITY_SELECT_SEPARATORS = "/^$"


class AttributeFilter(object):
	"""docstring for AttributeFilter"""
	def __init__(self, *args,**kwargs):
		super(AttributeFilter, self).__init__()
		print("filter with",args,kwargs)
		self.args = args
		self.kwargs = kwargs
			
	def _pick_byName(self,attribute):
		print("testing attribute with name filter",attribute,self.args,attribute['name'] in self.args)
		return attribute['name'] in self.args

	def _pick_nonID(self,attribute):
		return not attribute.get('is_id',False)



class EntityInput(Form):
	"""docstring for EntityInput"""
	def __init__(self, entity, display=None, no_labels=False, columns=None, picker=None, attributes=None, with_submit=False, input_owner=True, 
		**kwargs):
		super(EntityInput, self).__init__(**kwargs)
		self.table = Table();
		self.entity = entity
		self.no_labels = no_labels
		self.with_submit = with_submit
		self.input_owner = input_owner
		self.columns = columns if columns is not None else {}
		self.attributes = attributes if attributes is not None else {}

		displayed = self.pickColumns(picker,*(display if display is not None else []))

		self.build(displayed)

	def pickColumns(self,picker,*args,**kwargs):		
		if picker is None:
			if len(args) == 0:
				picker = lambda x:True
			else:
				picker = AttributeFilter(*args,**kwargs)._pick_byName
		elif type(picker) is str:
			picker = getattr(AttributeFilter(*args,**kwargs),f"_pick_{picker}")
		elif not hasattr(picker,"__call__"):
			raise Exception(f"{picker} must be a callable or a string referring to an existing picking method")

		displayed = []	
		for attr in self.entity.ATTRIBUTES:
			print("Testing attribute",attr,picker)
			if picker(attr):
				print("is picked",attr)
				displayed.append(attr['name'])
				
		return displayed

	def build(self,columns):

		if not self.no_labels:
			self.addChild(self.table)
			
		for attribute in self.entity.ATTRIBUTES:
			if attribute['name'] in columns:
				attr = AttributeInput.forAttribute(attribute['type'](
					no_check=True, **{k:v for k,v in attribute.items() if not (k in ["type","required"])}
				),**self.attributes.get(attribute['name'],{}))
				attr.placeholder = self.columns.get(attr.name,attr.name)
				if self.input_owner:
					attr.addData(["entity"],getattr(self.entity,"ENTITY_NAME",self.entity.__name__))
				if self.no_labels:
					self.addChild(attr,verify=False)
				else:
					self.table.addLines(TableLine(
						TableHeadCell(f"{self.columns.get(attr.name,attr.name)} : "), TableCell(None).addChild(attr)
					))
				super(EntityInput,self).addInput(attr)

		if self.with_submit:
			self.table.addLines(TableLine(
				TableHeadCell(None,align="center",colspan=2).addChild(Button("Submit",type="submit"))
			))


	def render(self, no_form=False):
		if no_form:
			return self.table.render()
		return super(EntityInput,self).render()



class EntitySelect(Select):
	"""docstring for EntitySelect"""
	def __init__(self, *entities, detailled=False, selector=None, **kwargs):
		super(EntitySelect, self).__init__(items=[
			(EntitySelect.getValue(entity),repr(entity)) for entity in entities
		],**kwargs)
		self.entities = entities
		self.selector = selector

	def getValue(entity):
		if self.selector is None:
			ids = [attr['name'] for attr in entity.ATTRIBUTES if attr.get('is_id',False)]
		separator = None
		for sep in ENTITY_SELECT_SEPARATORS:
			if any([sep in getattr(entity,id_) for id_ in ids]):
				continue
			separator = sep; break;
		if separator is None:
			raise Exception('No valid separator')
		return separator.join([getattr(entity,id_) for id_ in ids])+separator


	def render(self,ungroup=False):
		types = set([type(entity) for entity in self.entities])
		if len(types) > 1 and not ungroup:
			self.groups = [(type_,[self.items[i][0] for i,entity in self.entities if type(entity) == type_]) for type_ in types]
		return render(self)



class EntityList(Table):
	"""docstring for EntityList"""
	def __init__(self, *entities, entity_type=None, display=None, picker=None, columns=None, attributes=None, **kwargs):
		super(EntityList, self).__init__(**kwargs)
		columns = columns if columns is not None else {}
		attributes = {} if attributes is None else attributes;
		if entity_type is None:
			if len(set([type(entity) for entity in entities])) != 1:
				raise Exception("Entities list can't be empty or contain different types of entities")
			entity_type = type(entities[0])
		self.entity_type = entity_type
		display = [attr['name'] for attr in entity_type.ATTRIBUTES] if display is None else display
		displayed = self.pickColumns(picker,*display);
		self.setHead(TableHead(TableLine(
			*[TableHeadCell(columns.get(name,name)) for name in displayed]
		)))
		self.setBody(TableBody(*[TableLine(
			*[TableCell(attributes.get(name,{}).get(entity[name],entity[name])) for name in displayed]
		) for entity in entities]))

	def pickColumns(self,picker,*args,**kwargs):		
		if picker is None:
			if len(args) == 0:
				picker = lambda x:True
			else:
				picker = AttributeFilter(*args,**kwargs)._pick_byName
		elif type(picker) is str:
			picker = getattr(AttributeFilter(*args,**kwargs),f"_pick_{picker}")
		elif not hasattr(picker,"__call__"):
			raise Exception(f"{picker} must be a callable or a string referring to an existing picking method")

		displayed = []	
		for attr in self.entity_type.ATTRIBUTES:
			if picker(attr):
				displayed.append(attr['name'])

		return displayed

	def from_list(entities,*args,**kwargs):
		return EntityList(*entities,*args,**kwargs)