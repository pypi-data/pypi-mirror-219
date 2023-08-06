from temod.base import Entity, Join, Cluster 
from temod.storage import REGISTRED_STORAGES


class TemodLoginsException(Exception):
	pass


class TemodUserHandler(object):
	"""docstring for TemodUserHandler"""
	def __init__(self, user_class, database_type, identifier="id", logins=None, is_authenticated_attr="is_authenticated", is_active_attr= "is_active", 
		**db_credentials):
		super(TemodUserHandler, self).__init__()
		self.user_class = user_class
		self.is_authenticated_attr = is_authenticated_attr
		self.is_active_attr = is_active_attr
		self.db_credentials = db_credentials
		self.identifier = identifier
		self.logins = [] if logins is None else logins
		try:
			if issubclass(user_class,Entity):
				self.database = REGISTRED_STORAGES[database_type][Entity]
			elif issubclass(user_class,Join):
				self.database = REGISTRED_STORAGES[database_type][Join]
			elif issubclass(user_class,Cluster):
				self.database = REGISTRED_STORAGES[database_type][Cluster]
			else:
				raise
		except:
			raise Exception(f"Cannot pick the right database for user class {user_class} and database {database}")

	def load_user(self,x):
		dct = {self.identifier:x}
		return TemodUser(self.database(self.user_class,**self.db_credentials).get(**dct))

	def search_user(self,*logins):
		if len(logins) > len(self.logins):
			raise TemodLoginsException("There is more logins than expected")
		elif len(logins) < len(self.logins):
			raise TemodLoginsException("Some logins are missing")
		return TemodUser(self.database(self.user_class,**self.db_credentials).get(
			**{self.logins[i]:logins[i] for i in range(len(logins))}
		))

	def login_user(self,temod_user):
		temod_user.user.takeSnapshot()
		temod_user[self.is_authenticated_attr] = True
		temod_user[self.is_active_attr] = True
		return self.database(self.user_class,**self.db_credentials).updateOnSnapshot(temod_user.user)



class TemodUser(object):
	"""docstring for TemodUser"""
	def __init__(self,user,identifier="id"):
		super(TemodUser, self).__init__()
		self.identifier = identifier
		self.user = user

	def __getattribute__(self,name):
		if name != "user":
			if name == "is_authenticated":
				return self.user["is_authenticated"]
			elif name == "is_active":
				return self.user["is_active"]
			try:
				return self.user[name]
			except:
				pass
		try:
			return super(TemodUser,self).__getattribute__(name)
		except:
			return getattr(self.user,name)

	def get_id(self):
		return self.user[self.identifier]

	def __getitem__(self,name):
		return self.user[name]

	def __setitem__(self,name,value):
		self.user[name] = value