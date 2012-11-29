import os
import yaml
import new

class AConfig(object):

	def __init__(self, app=None, format='yaml'):
		if app is not None:
			self.app = app
			self.init_app(self.app, format)
		else:
			self.app = None
		
		self.format = format

	def init_app(self, app, format='yaml'):
		self.format = format
		self.app = app
		self.attach_loader()

	def attach_loader(self):
		method_name = 'from_' + self.format
		if method_name not in globals():
			raise Exception('The specified configuration format is not supported!')

		m = new.instancemethod(globals()[method_name], self.app.config, self.app.config.__class__)

		setattr(self.app.config, method_name, m)


def from_yaml(self, path):
	environment = os.getenv('APP_ENV', 'development').upper()
	self['ENVIRONMENT'] = environment.lower()

	with open(path) as p:
		y = yaml.load(p)

	e = y.get(environment, y)

	for k in e.iterkeys():
		if k.isupper():
			self[k] = e[k]
