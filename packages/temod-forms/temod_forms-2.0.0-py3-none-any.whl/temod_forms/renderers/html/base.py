import random

ATTRIBUTE_TRANSLATE = {
	"class_":"class"
}

class HTMLTag(object):
	"""docstring for HTMLTag"""
	def __init__(self, tag, id=None,class_=None,align=None):
		super(HTMLTag, self).__init__()
		self.__attributes__ = ["id","class_","align"]
		self.class_ = class_ if type(class_) is not list else " ".join(class_)
		self.dataset = []
		self.align = align
		self.tag = tag
		self.id = id
		self.children = []

	def addData(self,path,value):
		self.dataset.append((path,value))

	def addAttribute(self,attribute,value):
		if hasattr(self,attribute):
			raise Exception(f"Attribute {attribute} is already set")
		if not attribute in self.__attributes__:
			self.__attributes__.append(attribute)
		setattr(self,attribute,value)
		return self

	def addClass(self,class_):
		if self.class_ is None:
			self.class_ = f"{class_}"
		elif not (class_ in self.class_.split()):
			self.class_ += f" {class_}"
		return self

	def addChild(self,child,verify=True):
		if verify and not issubclass(type(child),HTMLTag):
			raise Exception("Added children must be subtype of HTMLTag")
		self.children.append(child)
		return self

	def insertChild(self,pos,child,verify=True):
		if verify and not issubclass(type(child),HTMLTag):
			raise Exception("Added children must be subtype of HTMLTag")
		self.children.insert(pos,child)
		return self

	def addChildren(self,*children,verify=True):
		if any([not issubclass(type(child),HTMLTag) for child in children]):
			raise Exception("Added children must be subtype of HTMLTag")
		self.children.extend(children)
		return self

	def insertChildren(self,pos,*children,verify=True):
		if verify and any([not issubclass(type(child),HTMLTag) for child in children]):
			raise Exception("Added children must be subtype of HTMLTag")
		self.children = self.children[:pos]+list(children)+self.children[pos:]
		return self

	def decorate(self,decorator,*args,**kwargs):
		return decorator.decorate(self,*args,**kwargs)

	def open(self):
		attributes = " ".join([
			f'{ATTRIBUTE_TRANSLATE.get(attr,attr)}="{getattr(self,attr)}"' for attr in self.__attributes__ if getattr(self,attr,None) is not None
		])
		if len(self.dataset) > 0:
			attributes += " "+" ".join([
				'data-'+"".join([name.lower().title() for name in path])+f"={value}" for path,value in self.dataset
			])
		return f"<{self.tag} {attributes}>"

	def close(self):
		return f"</{self.tag}>"

	def render(self, innerHTML=None, close=True):
		if innerHTML is None:
			innerHTML = "".join([child.render() for child in self.children])
		if close:
			return f"{self.open()}{innerHTML}</{self.tag}>"
		return self.open()


class Div(HTMLTag):
	"""docstring for Div"""
	def __init__(self, **kwargs):
		super(Div, self).__init__("div", **kwargs)


class H1(HTMLTag):
	"""docstring for H1"""
	def __init__(self, text, **kwargs):
		super(H1, self).__init__("h1", **kwargs)
		self.text = text

	def render(self):
		return super(H1,self).render(innerHTML=self.text)


class Input(HTMLTag):
	"""docstring for Input"""
	def __init__(self, name=None, value=None, placeholder=None, tag="input", **kwargs):
		super(Input, self).__init__(tag, **kwargs)
		self.__attributes__.extend(["name","value","placeholder","type"])
		self.placeholder = placeholder
		self.value = value
		self.name = name

	def render(self,*args,close=False,**kwargs):
		return super(Input,self).render(*args,close=close,**kwargs)


class NumericInput(Input):
	"""docstring for NumericInput"""
	def __init__(self, step=1, min=None, max=None, **kwargs):
		super(NumericInput, self).__init__(**kwargs)
		self.__attributes__.extend(["step","min","max"])
		self.type = "number"
		self.step = step
		self.min = min
		self.max = max


class TextInput(Input):
	"""docstring for TextInput"""
	def __init__(self, min=None, max=None, **kwargs):
		super(TextInput, self).__init__(**kwargs)
		self.__attributes__.extend(["min","max"])
		self.type = "text"
		self.min = min
		self.max = max


class TextAreaInput(Input):
	"""docstring for TextAreaInput"""
	def __init__(self, min=None, max=None, **kwargs):
		super(TextAreaInput, self).__init__(tag="textarea",**kwargs)
		self.__attributes__.extend(["min","max"])
		self.type = "text"
		self.min = min
		self.max = max

	def render(self):
		innerHTML = self.value if self.value is not None else ""
		return super(TextAreaInput,self).render(innerHTML=innerHTML,close=True)


class DateInput(Input):
	"""docstring for DateInput"""
	def __init__(self, **kwargs):
		super(DateInput, self).__init__(**kwargs)
		self.type = "date"


class TimeInput(Input):
	"""docstring for TimeInput"""
	def __init__(self, **kwargs):
		super(TimeInput, self).__init__(**kwargs)
		self.type = "time"


class DateTimeInput(Input):
	"""docstring for DateTimeInput"""
	def __init__(self, **kwargs):
		super(DateTimeInput, self).__init__(**kwargs)
		self.type = "datetime-local"


class Select(Input):
	"""docstring for Select"""
	def __init__(self, *items, groups=None, **kwargs):
		super(Select, self).__init__(tag="select", **kwargs)
		self.__attributes__.extend(["name"])
		self.options = [Option(value=item[0],text=item[1]) for item in items]
		self.groups = groups

	def render(self,include_attributes=None):
		if self.groups is not None:
			innerHTML = "".join([
				f"<optgroup label={group[0]}>"+"".join([
					option.render() for option in self.options if option.value in group[1]
				]+"</optgroup>")
				for group in self.groups
			])
		else:
			innerHTML = "".join([option.render() for option in self.options if option.value is not None])
		return super(Select,self).render(innerHTML=innerHTML,close=True)


class Option(HTMLTag):
	"""docstring for Option"""
	def __init__(self, value, text, **kwargs):
		super(Option, self).__init__("option", **kwargs)
		self.__attributes__.extend(["value"])
		self.value = value
		self.text = text

	def render(self,include_attributes=None):
		return super(Option,self).render(innerHTML=self.text)


class Button(HTMLTag):
	"""docstring for Button"""
	def __init__(self, text, type="button", **kwargs):
		super(Button, self).__init__("button", **kwargs)
		self.__attributes__.extend(["type"])
		self.type = type
		self.text = text

	def render(self):
		if len(self.children) == 0:
			text = "" if self.text is None else self.text
			return super(Button,self).render(innerHTML=text)
		return super(Button,self).render()


class Form(HTMLTag):
	"""docstring for Form"""
	def __init__(self, method=None, action="javascript:void(0);", enctype=None, prefix=None, values=None, onsubmit=None, **kwargs):
		super(Form, self).__init__("form",**kwargs)
		self.__attributes__.extend(["method","action","enctype","onsubmit"])
		self.values = {} if values is None else values
		self.onsubmit = onsubmit
		self.enctype = enctype
		self.method = method
		self.action = action
		self.prefix = prefix
		self.inputs = []
		if enctype == "json" or (method is not None and method.lower() not in ["get","post"]):
			func_name = self.jsonForm(action)
			self.onsubmit = f"{func_name}(this);"
			self.enctype = None
			self.action = "javascript:void(0);";

	def addInput(self,input_):
		assert(issubclass(type(input_),Input) or issubclass(type(input_),Select))
		if self.prefix is not None and input_.name is not None:
			input_.name = self.prefix + input_.name
		input_.value = self.values.get(input_.name,None)
		self.inputs.append(input_)

	def generateFuncName(self):
		LETTERS = "abcdefghijklmnopqrstuvwxyz"
		ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"
		return LETTERS[random.randint(0,len(LETTERS)-1)]+''.join([ALPHABET[random.randint(0,len(ALPHABET)-1)] for _ in range(20)])

	def jsonForm(self,url):
		func_name = self.generateFuncName()
		method_name = self.method.upper()
		onload = "try{ req.onload = TEMOD.FormReponse('json'); }catch(e){ console.log('Do not forget to include the temod js script') }"
		self.addChild(Script(content=f"""function {func_name}(form_)"""+"{"+f"""
			var req = new XMLHttpRequest();
			{onload}
			req.open("{method_name}","{url}");
			req.setRequestHeader("Content-Type","application/json");
			req.send(JSON.stringify(Object.fromEntries(new FormData(form_).entries())))
		"""+"}"))
		return func_name



class TableCell(HTMLTag):
	"""docstring for TableCell"""
	def __init__(self, text, tag="td", colspan=None, **kwargs):
		super(TableCell, self).__init__(tag,**kwargs)
		self.__attributes__.extend(["colspan"])
		self.colspan = colspan
		self.text = text

	def render(self):
		if len(self.children) == 0:
			text = "" if self.text is None else self.text
			return super(TableCell,self).render(innerHTML=text)
		return super(TableCell,self).render()


class TableHeadCell(TableCell):
	"""docstring for TableHeadCell"""
	def __init__(self, text, **kwargs):
		super(TableHeadCell, self).__init__(text, tag="th",**kwargs)


class TableLine(HTMLTag):
	"""docstring for TableLine"""
	def __init__(self, *cells, **kwargs):
		super(TableLine, self).__init__("tr",**kwargs)
		if len(cells) > 0:
			self.addChildren(*cells)

	def addCell(self,cell):
		if issubclass(type(cell),TableCell):
			raise Exception("TableLine children must be subtype of TableCell")
		return super(TableLine,self).addChild(cell,verify=False)

	def insertCell(self,pos,cell):
		if issubclass(type(cell),TableCell):
			raise Exception("TableLine children must be subtype of TableCell")
		return super(TableLine,self).insertChild(pos,cell,verify=False)

	def addCells(self,*cells):
		if any([not issubclass(type(cell),TableCell) for cell in cells]):
			raise Exception("TableLine children must be subtype of TableCell")
		return super(TableLine,self).addChildren(*cells,verify=False)

	def insertCells(self,pos,*cells):
		if any([not issubclass(type(cell),TableCell) for cell in cells]):
			raise Exception("TableLine children must be subtype of TableCell")
		return super(TableLine,self).addChildren(pos,*cells,verify=False)
		

class TableHead(HTMLTag):
	"""docstring for TableHead"""
	def __init__(self, *lines ,**kwargs):
		super(TableHead, self).__init__("thead",**kwargs)
		if any([not issubclass(type(line),TableLine) for line in lines]):
			raise Exception("TableHead children must be subtype of TableLine")
		if len(lines) > 0:
			self.addChildren(*lines)

	def addChild(self,child):
		if issubclass(type(child),TableLine):
			raise Exception("TableHead children must be subtype of TableLine")
		return super(TableHead,self).addChild(child,verify=False)

	def insertChild(self,pos,child):
		if issubclass(type(child),TableLine):
			raise Exception("TableHead children must be subtype of TableLine")
		return super(TableHead,self).insertChild(pos,child,verify=False)

	def addChildren(self,*children):
		if any([not issubclass(type(child),TableLine) for child in children]):
			raise Exception("TableHead children must be subtype of TableLine")
		return super(TableHead,self).addChildren(*children,verify=False)

	def insertChildren(self,pos,*children):
		if any([not issubclass(type(child),TableLine) for child in children]):
			raise Exception("TableHead children must be subtype of TableLine")
		return super(TableHead,self).addChildren(pos,*children,verify=False)
		

class TableBody(HTMLTag):
	"""docstring for TableBody"""
	def __init__(self, *lines ,**kwargs):
		super(TableBody, self).__init__("tbody",**kwargs)
		if any([not issubclass(type(line),TableLine) for line in lines]):
			raise Exception("TableBody children must be subtype of TableLine")
		if len(lines) > 0:
			self.addChildren(*lines)

	def addChild(self,child):
		if issubclass(type(child),TableLine):
			raise Exception("TableBody children must be subtype of TableLine")
		return super(TableBody,self).addChild(child,verify=False)

	def insertChild(self,pos,child):
		if issubclass(type(child),TableLine):
			raise Exception("TableBody children must be subtype of TableLine")
		return super(TableBody,self).insertChild(pos,child,verify=False)

	def addChildren(self,*children):
		if any([not issubclass(type(child),TableLine) for child in children]):
			raise Exception("TableBody children must be subtype of TableLine")
		return super(TableBody,self).addChildren(*children,verify=False)

	def insertChildren(self,pos,*children):
		if any([not issubclass(type(child),TableLine) for child in children]):
			raise Exception("TableBody children must be subtype of TableLine")
		return super(TableBody,self).addChildren(pos,*children,verify=False)
		

class Table(HTMLTag):
	"""docstring for Table"""
	def __init__(self, *lines ,**kwargs):
		super(Table, self).__init__("table",**kwargs)
		self.thead = None
		self.tbody = None
		if len(lines) > 0:
			self.addLines(*lines)

	def setHead(self,thead):
		if not issubclass(type(thead),TableHead):
			raise Exception("Table head must be subtype of TableHead")
		self.thead = thead
		self.children = [x for x in [self.thead,self.tbody] if x is not None]

	def setBody(self,tbody):
		if not issubclass(type(tbody),TableBody):
			raise Exception("Table head must be subtype of TableBody")
		self.tbody = tbody
		self.children = [x for x in [self.thead,self.tbody] if x is not None]

	def addLines(self,*lines):
		if self.tbody is None:
			self.setBody(TableBody(*lines))
		else:
			self.tbody.addChildren(*lines)

	def insertLines(self,pos,*lines):
		if self.tbody is None:
			self.setBody(TableBody(*lines))
		else:
			self.tbody.insertChildren(pos,*lines)

	def render(self):
		if self.thead is not None:
			innerHTML = self.thead.render()
			if self.tbody is not None:
				innerHTML += self.tbody.render()
			else:
				innerHTML += TableBody(*self.lines).render()
		else:
			if self.tbody is not None:
				innerHTML = self.tbody.render()
			else:
				innerHTML = "".join([line.render() for line in self.children])

		return super(Table,self).render(innerHTML=innerHTML)


class Script(HTMLTag):
	"""docstring for Script"""
	def __init__(self, src=None, content="", **kwargs):
		super(Script, self).__init__("script", **kwargs)
		self.__attributes__.extend(["src"])
		self.content = content
		self.src = src

	def render(self):
		return super(Script,self).render(innerHTML=self.content)



		


		
		