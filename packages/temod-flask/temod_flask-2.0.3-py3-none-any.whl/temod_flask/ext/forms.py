from temod_forms.readers.dict_reader import *
from temod.base.attribute import *

class FormReadersException(Exception):
	pass


class FormReadersHolder(object):
	"""docstring for FormReadersHolder"""
	def __init__(self):
		super(FormReadersHolder, self).__init__()
		self.entities = {}
		self.joins = {}
		self.clusters = {}

	def addEntity(self,entity):
		self.entities[entity.__name__] = EntityDictReader(entity)

	def addJoin(self,join):
		self.joins[join.__name__] = JoinDictReader(join)

	def addCluster(self,cluster):
		self.clusters[cluster.__name__] = ClusterDictReader(cluster)

	##########################################

	def single(self,name, **z):
		if name in self.entities and not "date_fields" in z:
			z["date_fields"] = [
				attr['name'] for attr in self[name].entity_type.ATTRIBUTES 
				if attr['type'] in [DateAttribute,DateTimeAttribute]
			]
		return lambda *x,**y: self[name].read(*x,**y, **z)

	##########################################

	def __getitem__(self,name):
		obj_ = self.entities.get(
			name,self.joins.get(
				name,self.clusters.get(name,None)
			)
		)
		if obj_ is not None:
			return obj_
		raise FormReadersException(f"Unknown object {name}.")


_readers_holder = FormReadersHolder()
		