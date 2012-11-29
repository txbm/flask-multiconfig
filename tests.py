import os
import unittest
import flask

from flask_aconfig import AConfig

class TestFlaskAConfig(unittest.TestCase):

	def setUp(self):
		self.app = flask.Flask(__name__)
		a = AConfig()
		a.init_app(self.app)

	def test_from_yaml(self):
		self.app.config.from_yaml('test_config.yml')
		self.assertEqual(self.app.config['ENVIRONMENT'], 'development')

		os.environ['APP_ENV'] = 'testing'
		self.app.config.from_yaml('test_config.yml')
		self.assertEqual(self.app.config['ENVIRONMENT'], 'testing')
		self.assertEqual(self.app.config['TESTING'], True)

if __name__ =='__main__':
    unittest.main()
