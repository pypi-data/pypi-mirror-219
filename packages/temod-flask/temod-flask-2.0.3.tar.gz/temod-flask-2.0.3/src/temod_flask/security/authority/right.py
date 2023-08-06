from temod.base.attribute import StringAttribute
from temod.storage.directory import YamlStorage
from temod.base.entity import Entity

from .exceptions import *
from .utils import *



class AccessRight(Entity):
	"""docstring for AccessRight"""
	ENTITY_NAME = "right"
	ATTRIBUTES = {}
	def __init__(self, label, **kwargs):
		super(AccessRight, self).__init__(StringAttribute("label",value=label,force_lower_case=False,is_nullable=False,non_empty=True))
		self.infos = kwargs

	def __getitem__(self,attr):
		try:
			return self.infos[attr]
		except:
			pass
		return super(AccessRight,self).__getitem__(attr)



class LawBook(object):
	"""docstring for LawBook"""
	def __init__(self, rights):
		super(LawBook, self).__init__()
		self.rights = {}
		for right in rights:
			self.add_right(right)

	def add_right(self,right):
		try_assert(
			issubclass(type(right),AccessRight),MalformedLawBookError,"Added rights must be subclass of AccessRight"
		)
		try_assert(
			not (right['label'] in self.rights),MalformedLawBookError,f"Right with label '{right['label']}' is already registered"
		)
		self.rights[right['label']] = right

	def list_rights(self):
		return self.rights.values()

	def to_dict(self):
		return {
			label:right.infos for label,right in self.rights.items()
		}



class YamlLawBookKeeper(YamlStorage):
	"""docstring for YamlLawBookKeeper"""
	def __init__(self,filename, directory, encoding="utf-8", final=True):
		super(YamlLawBookKeeper, self).__init__(
			directory,encoding=encoding
		)
		self.filename = filename
		self.final = final

	def load(self):
		loaded = super(YamlLawBookKeeper,self).load(self.filename)
		if type(loaded) is list:
			self.lawBook = LawBook([
				AccessRight(element.pop('label'),**element) for element in loaded
			])
		elif type(loaded) is dict:
			self.lawBook = LawBook([
				AccessRight(label,**element) for label,element in loaded.items()
			])
		else:
			raise MalformedLawBookError("Stored access rights must be in the format list of dictionnaries or a dictionnary")
		return self.lawBook
		
	def save(self):
		if self.final:
			raise ImmutableLawBookError("Cannot overwrite saved access rights")
		return super(YamlLawBookKeeper,self).save(self.filename,self.lawBook.to_dict())