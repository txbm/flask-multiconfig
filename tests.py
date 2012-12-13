import os
import unittest
import flask

from flask.ext.aconfig import AConfig, Schema, Yaml, HerokuEnv

class TestFlaskAConfig(unittest.TestCase):

	def setUp(self):
		self.app = flask.Flask(__name__)
		self.app.config.setdefault('ENV', 'local')
		self.app.config.setdefault('MODE', 'development')
		self.a = AConfig(self.app)

	def test_yaml(self):
		Schema('local', 'development', Yaml('test_config.yml', 'DEV'), self.a)
		self.a.reload()

		self.assertEqual(self.app.config.get('SQLALCHEMY_DATABASE_URI'), 'mysql://root:1234@127.0.0.1/dev_db')

	def test_herokuenv(self):
		Schema('heroku', 'development', HerokuEnv(['SQL_ALCHEMY']), self.a)
		self.app.config['ENV'] = 'heroku'
		os.environ['DATABASE_URL'] = 'mysql://not:real@nowhere.com/herp'
		self.a.reload()

		self.assertEqual(self.app.config.get('SQLALCHEMY_DATABASE_URI'), 'mysql://not:real@nowhere.com/herp')

	def test_cascade(self):
		Schema('local', 'development', Yaml('test_config.yml', 'DEV'), self.a)
		Schema('local', 'development', HerokuEnv('SQL_ALCHEMY'), self.a)
		os.environ['DATABASE_URL'] = 'mysql://not:real@nowhere.com/herp'
		self.a.reload()

		self.assertEqual(self.app.config.get('SQLALCHEMY_DATABASE_URI'), 'mysql://not:real@nowhere.com/herp')

	def test_cascade_defer(self):
		Schema('local', 'development', Yaml('test_config.yml', 'DEV'), self.a)
		Schema('local', 'development', HerokuEnv('SQL_ALCHEMY'), self.a)
		del os.environ['DATABASE_URL']
		self.a.reload()

		self.assertEqual(self.app.config.get('SQLALCHEMY_DATABASE_URI'), 'mysql://root:1234@127.0.0.1/dev_db')		

if __name__ =='__main__':
    unittest.main()
