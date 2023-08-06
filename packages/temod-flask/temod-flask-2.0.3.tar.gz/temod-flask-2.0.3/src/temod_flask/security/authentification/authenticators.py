from flask_login import LoginManager, login_user
from flask import request, redirect

from oauthlib.oauth2 import WebApplicationClient
from functools import partial
import requests
import json

from .exceptions import *


class Authenticator(LoginManager):
	"""docstring for Authenticator"""
	def __init__(self, loader, postload=None, login_view="login", **kwargs):
		super(Authenticator, self).__init__(**kwargs)
		self.login_view = login_view
		self.setLoader(loader)
		self.postload = None;
		if postload is not None:
			self.setPostLoader(postload)

	def search_user(self,*logins):
		return self.loader.search_user(*logins)

	def login_user(self,user):
		self.loader.login_user(user)
		print(user)
		return login_user(user)

	def setLoader(self,loader):
		self.loader = loader
		@self.user_loader
		def load(userID):
			loaded_user = self.loader.load_user(userID)
			if loaded_user is None or self.postload is None:
				return loaded_user
			return self.postload(loaded_user)

	def setPostLoader(self,post_loader):
		try:
			assert(hasattr(post_loader,"__call__"))
		except:
			raise MalformedAuthenticatorError("The user post loader must be a callable object.")
		self.postload = post_loader



class OAuth2WebAuthenticator(Authenticator):
	"""docstring for OAuth2WebAuthenticator"""
	def __init__(self, application_id, application_secret, discovery_url, *args, default_scope = None, user_class = None,
			configs_authorization_edp = "authorization_endpoint", configs_token_edp = "token_endpoint", configs_infos_edp="userinfo_endpoint",
			**kwargs
		):
		super(OAuth2WebAuthenticator, self).__init__(user_class,*args, **kwargs)

		self.application_id = application_id
		self.application_secret = application_secret
		self.discovery_url = discovery_url
		self.configs_authorization_edp = configs_authorization_edp
		self.configs_token_edp = configs_token_edp
		self.configs_infos_edp = configs_infos_edp
		self.default_scope = default_scope

		self.client = WebApplicationClient(application_id)

	def getAuthentificatorConfig(self,field=None):
		dct = requests.get(self.discovery_url).json()
		if field is None:
			return dct
		return dct[field]

	def create_authentification_endpoint(self,name,scope,callback_address=None):

		def endpointFunction(host,route):
			authorization_endpoint = self.getAuthentificatorConfig(field=self.configs_authorization_edp)
			if host is None:
				host = f"https://{request.environ['HTTP_HOST']}"
			request_uri = self.client.prepare_request_uri(
				authorization_endpoint,
				redirect_uri=host+route,
				scope=scope,
			)
			return redirect(request_uri)

		function = partial(endpointFunction,*callback_address)
		function.__name__ = name+"_auth"
		return function

	def create_callback_endpoint(self,name,loader=None):
		def endpointFunction():
			code = request.args.get("code")
			token_endpoint = self.getAuthentificatorConfig(field=self.configs_token_edp)
			token_url, headers, body = self.client.prepare_token_request(
				token_endpoint,
				authorization_response=request.url,redirect_url=request.base_url,code=code
			)
			token_response = requests.post(
				token_url,headers=headers,data=body,
				auth=(self.application_id, self.application_secret),
			)

			self.client.parse_request_body_response(json.dumps(token_response.json()))
			userinfo_endpoint = self.getAuthentificatorConfig(field=self.configs_infos_edp)
			uri, headers, body = self.client.add_token(userinfo_endpoint)
			userinfos = requests.get(uri, headers=headers, data=body).json()

			if loader is None:
				return self.loading_function(userinfos)
			return loader(userinfos)

		endpointFunction.__name__ = name+"_callback"
		return endpointFunction

	def OAUTH2endpoint(self,app,label,route,callback_route=None,callback_host=None,scope=None):
		if scope is None:
			scope = self.default_scope
		if callback_route is None:
			callback_route = f"{route}/callback"
		def __auth(function):
			app.route(f'{route}')(self.create_authentification_endpoint(label,scope,callback_address=(callback_host,callback_route)))
			app.route(f"{callback_route}")(self.create_callback_endpoint(label,loader=function))
		return __auth

	def init_app(self,app,routes=None):
		if routes is None:
			routes = []

		for route in routes:

			if not "callback" in route:
				route['callback'] = f"{route['url']}/callback"

			app.route(f'{route["url"]}')(
				self.create_authentification_endpoint(route['name'],route.get('scope',self.default_scope),route["callback"])
			)

			app.route(f"{route['callback']}")(
				self.create_callback_endpoint(route['name'],route['callback'],loader=route.get('user_loader',None))
			)



		

		