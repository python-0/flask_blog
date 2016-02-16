import os
basedir = os.path.abspath( os.path.dirname(__file__) )


class Config:
	SECRET_KEY = 'hard to guess string'

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True

	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'keeporder@163.com'
	MAIL_PASSWORD = 'Aa1234567'
	FLASKY_ADMIN = 'li.dinglong@163.com'
	FLASKY_MAIL_PREFIX = '[Flask]'

	@staticmethod
	def init_app(app):
		pass

	def __init__(self):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development': 		DevelopmentConfig,
	'testing': 			TestingConfig,
	'ProductionConfig':	ProductionConfig,
	'default':			DevelopmentConfig
}
