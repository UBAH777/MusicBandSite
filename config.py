import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a really really really really long secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopementConfig(BaseConfig):
    DEBUG = True
    db_name = 'band.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
                  f'sqlite:///{app_dir}/{db_name}'


class TestingConfig(BaseConfig):
    DEBUG = True
    db_name = 'band.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
			      f'sqlite:///{app_dir}/{db_name}'


class ProductionConfig(BaseConfig):
    DEBUG = False
    db_name = 'band.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                  f'sqlite:///{app_dir}/{db_name}'