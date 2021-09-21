import os 

basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hardtoguessstring'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'memo.py'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):    
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite') 
    FLASK_DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    FLASK_DEBUG = False

config = {
    'development': DevelopmentConfig, 
    'production': ProductionConfig, 
    'default': DevelopmentConfig
}