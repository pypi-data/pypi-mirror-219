from temod.base.join import Join
from .entity import *
from .input import *
from .base import *


class EntityAttributeFilter(object):
	"""docstring for EntityAttributeFilter"""
	def __init__(self, *args,**kwargs):
		super(EntityAttributeFilter, self).__init__()
		print("EntityAttributeFilter with",args,kwargs)
		self.args = args
		self.kwargs = kwargs
			
	def _pick_byName(self,entity,attribute):
		entity_name = getattr(entity,"ENTITY_NAME",entity.__name__)
		for arg in self.args:
			if arg[0] != entity_name:
				continue
			return attribute['name'] in arg[1]
		return False

	def _pick_nonID(self,entity,attribute):
		return not attribute.get('is_id',False)


class JoinList(Table):
	"""docstring for JoinList"""
	def __init__(self, *joins, join_type=None, display=None, columns=None, picker=None, **kwargs):
		super(JoinList, self).__init__(**kwargs)
		columns = columns if columns is not None else {}
		display = display if display is not None else []
		if join_type is None:
			if len(set([type(entity) for entity in joins])) != 1:
				raise Exception("Entities list can't be empty or contain different types of joins")
			join_type = type(joins[0])

		self.join_type = join_type
		displayed = self.pickColumns(picker,*display);

		self.setHead(TableHead(TableLine(
			*[TableHeadCell(
				columns.get(column[0],{}).get(column[1],columns.get(column[1],column[1]))
			) for column in displayed]
		)))
		get_attr = lambda j,x,y: j[x][y] if j[x] is not None else None
		self.setBody(TableBody(*[TableLine(
			*[TableCell(get_attr(join,column[0],column[1])) for column in displayed]
		) for join in joins]))

	def definePicker(self,picker,*args,**kwargs):
		if picker is None:
			if len(args) == 0:
				picker = lambda x:True
			else:
				picker = EntityAttributeFilter(*args,**kwargs)._pick_byName			
		elif type(picker) is str:
			if picker == "shortcuts":
				p_args = []; temp = {}
				for shortcut,target in getattr(self.join_type,'SHORTCUTS',{}).items():
					entity, attribute = target.split('.')
					if not (entity in [arg[0] for arg in p_args]):
						p_args.append((entity,[])); temp[entity] = len(p_args)-1
					p_args[temp[entity]][1].append(attribute)
				picker = EntityAttributeFilter(*p_args,**kwargs)._pick_byName
			else:
				picker = getattr(EntityAttributeFilter(*args,**kwargs),f"_pick_{picker}")
		elif not hasattr(picker,"__call__"):
			raise Exception(f"{picker} must be a callable or a string referring to an existing picking method")
		return picker

	def pickColumns(self,picker,*args,**kwargs):	
		picker = self.definePicker(picker,*args,**kwargs)
		entity_types = [getattr(self.join_type, "DEFAULT_ENTRY", self.join_type.STRUCTURE[0].attributes[0].owner_type)]; columns = []
		for constraint in self.join_type.STRUCTURE:
			for attr in constraint.attributes:
				if not attr.owner_type in entity_types:
					entity_types.append(attr.owner_type)
		for entity_type in entity_types:
			entity_name = getattr(entity_type,"ENTITY_NAME",entity_type.__name__)
			for attribute in entity_type.ATTRIBUTES:
				if picker(entity_type,attribute):
					columns.append((entity_name,attribute['name']))
		return columns

	def from_list(joins,display=None,**kwargs):
		return JoinList(*joins,display=display,**kwargs)



class JoinInput(Form):
	"""docstring for JoinInput"""
	def __init__(self, join_type, display=None, no_labels=False, no_titles=False, columns=None, divisions=None, picker=None, with_submit=False, **kwargs):
		kwargs.pop('enctype',None); kwargs.pop('onsubmit',None); 
		func_name, script = self.jsonForm(kwargs.pop('action',"/"))
		super(JoinInput, self).__init__(action="javascript:void(0);",onsubmit=f"{func_name}(this);",enctype=None,**kwargs)
		self.addChild(script)
		self.table = None
		self.join_type = join_type
		self.no_labels = no_labels
		self.no_titles = no_titles
		self.with_submit = with_submit
		self.columns = columns if columns is not None else {}
		self.divisions = divisions if divisions is not None else {}
		self.inputs = []

		displayed = self.pickColumns(picker,*(display if display is not None else []));

		self.build(displayed)

	def definePicker(self,picker,*args,**kwargs):
		if picker is None:
			if len(args) == 0:
				picker = lambda x:True
			else:
				picker = EntityAttributeFilter(*args,**kwargs)._pick_byName			
		elif type(picker) is str:
			if picker == "shortcuts":
				p_args = []; temp = {}
				for shortcut,target in getattr(self.join_type,'SHORTCUTS',{}).items():
					entity, attribute = target.split('.')
					if not (entity in [arg[0] for arg in p_args]):
						p_args.append((entity,[])); temp[entity] = len(p_args)-1
					p_args[temp[entity]][1].append(attribute)
				picker = EntityAttributeFilter(*p_args,**kwargs)._pick_byName
			else:
				picker = getattr(EntityAttributeFilter(*args,**kwargs),f"_pick_{picker}")
		elif not hasattr(picker,"__call__"):
			raise Exception(f"{picker} must be a callable or a string referring to an existing picking method")
		return picker

	def pickColumns(self,picker,*args,**kwargs):	
		picker = self.definePicker(picker,*args,**kwargs)
		entity_types = [getattr(self.join_type, "DEFAULT_ENTRY", self.join_type.STRUCTURE[0].attributes[0].owner_type)]; columns = []
		for constraint in self.join_type.STRUCTURE:
			for attr in constraint.attributes:
				if not attr.owner_type in entity_types:
					entity_types.append(attr.owner_type)
		for entity_type in entity_types:
			for attribute in entity_type.ATTRIBUTES:
				if picker(entity_type,attribute):
					columns.append((entity_type,attribute['name']))
		return columns

	def jsonForm(self,url):
		func_name = self.generateFuncName()
		onload = "try{ req.onload = TEMOD.FormReponse('json'); }catch(e){ console.log('Do not forget to include the temod js script') }"
		return func_name, Script(content=f"""function {func_name}(form_)"""+"{"+f"""
			let req = new XMLHttpRequest();
			let inputs = Object.values(form_.getElementsByTagName('select')).map(x => x);
			Object.values(form_.getElementsByTagName('textArea')).forEach(x => inputs.push(x));
			Object.values(form_.getElementsByTagName('input')).forEach(x => inputs.push(x));
			let entities = inputs.map(x => x.dataset.entity)
			let i = 0; entities.filter(y => entities.indexOf(y) == (++i-1));
			let data = Object.fromEntries(
				entities.map(entity => [entity,Object.fromEntries(
					inputs.filter(input_ => input_.dataset.entity == entity).map(input_ => [input_.name,input_.value])
				)])
			)
			console.log(data)
			{onload}
			req.open("POST","{url}");
			req.setRequestHeader("Content-Type","application/json");
			req.send(JSON.stringify(data))
		"""+"}")

	def build(self,columns):
		entities = [getattr(self.join_type, "DEFAULT_ENTRY", self.join_type.STRUCTURE[0].attributes[0].owner_type)]; 
		displayed = {entities[0]:[]}
		for column in columns:
			if column[0] not in entities:
				entities.append(column[0])
				displayed[column[0]] = []
			displayed[column[0]].append(column[1])
		for entity in entities:
			div = Div()
			input_ = EntityInput(
				entity,picker=None,display=displayed[entity],input_owner=True,
				columns=self.columns.get(entity,self.columns.get(getattr(entity,"ENTITY_NAME",entity.__name__),{}))
			)
			if not self.no_titles:
				name = getattr(entity,"ENTITY_NAME",entity.__name__)
				div.addChild(H1(self.divisions.get(name,name)))
			table = input_.table
			if len(table.children) > 0:
				div.addChild(table)
			self.addChild(div)
		if self.with_submit:
			self.addChild(Div())
			self.children[-1].addChild(Button("Submit",type="submit"))