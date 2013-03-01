import yaml
import os


class AConfig(object):

	def __init__(self, app=None, schemas=[]):
		self.schemas = schemas
		
		if app is not None:
			self.app = app
			self.init_app(self.app)
		else:
			self.app = None


	def init_app(self, app):
		self.app = app
		self.reload()

	def reload(self):
		if not self.schemas:
			return False

		self.mode = self.app.config.get('MODE', 'development')
		self.env = self.app.config.get('ENV', 'local')

		loaded = []
		for schema in self.schemas:
			if schema.mode == self.mode and schema.env == self.env:
				schema.load(self.app)
				loaded.append(schema)

		if not loaded:
			raise Exception('No configuration schemas were selected!')

class Schema(object):

	def __init__(self, env, mode, source, aconfig=None):
		self.env = env
		self.mode = mode
		self.source = source
		if aconfig:
			aconfig.schemas.append(self)

	def load(self, app):
		kvps = self.source.load()
		if kvps:
			for k, v in kvps.iteritems():
				app.config[k] = v
			return True
		
		return False

class Source(object):

	def load(self, app):
		pass

class Yaml(Source):

	def __init__(self, path, section):
		self.path = path
		self.section = section

	def load(self):
		if not os.path.exists(self.path):
			return None
		
		kvps = {}
		with open(self.path) as p:
			y = yaml.load(p)

			s = y.get(self.section, y)

			for k in s.iterkeys():
				if k.isupper():
					kvps[k] = s[k]
		
		return kvps

# this needs some slight rethinking-- basically there needs to be a layer of indirection between SERVICE and LIBRARY. So for example, SQLALCHEMY_URL and DATABASE_URL are not the same thing. Ya feel me?

class HerokuEnv(Source):

	services_available = {
		'AMAZON_RDS': {
			'SQLALCHEMY_DATABASE_URI': 'DATABASE_URL'
		},
		'SENTRY_DSN': {
			'SENTRY_DSN': 'SENTRY_DSN'
		},
		'EXCEPTIONAL': {
			'EXCEPTIONAL_API_KEY': 'EXCEPTIONAL_API_KEY'
		},
		'GOOGLE_DOMAIN': {
			'GOOGLE_DOMAIN': 'GOOGLE_DOMAIN'
		},
		'RABBIT_MQ': {
			'BROKER_URL': 'RABBITMQ_URL'
		},
		'MAILGUN': {
			'SMTP_SERVER': 'MAILGUN_SMTP_SERVER',
			'SMTP_LOGIN': 'MAILGUN_SMTP_LOGIN',
			'SMTP_PASSWORD': 'MAILGUN_SMTP_PASSWORD'
		},
		'REDIS': {
			'REDIS_URL': 'REDISTOGO_URL'
		},
		'MONGOLAB': {
			'MONGO_URL': 'MONGOLAB_URI'
		},
		'MONGOHQ': {
			'MONGO_URL': 'MONGOHQ_URL'
		},
		'MEMCACHIER': {
			'MEMCACHED_SERVERS': 'MEMCACHIER_SERVERS',
			'MEMCACHED_USERNAME': 'MEMCACHIER_USERNAME',
			'MEMCACHED_PASSWORD': 'MEMCACHIER_PASSWORD'
		},
		'POSTGRES': {
			'SQLALCHEMY_DATABASE_URI': 'DATABASE_URL'
		}
	}

	services_enabled = []

	def __init__(self, services=None):
		if isinstance(services, str):
			services = [services]

		self.services_enabled = services

	def load(self):
		if not self.services_enabled:
			return None

		kvps = {}
		for service in self.services_enabled:
			if service in self.services_available:
				for k, v in self.services_available[service].iteritems():
					envar = os.environ.get(v, None)
					if envar:
						kvps[k] = envar

		return kvps