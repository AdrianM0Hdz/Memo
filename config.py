import os 

basedir = os.path.abspath(__name__)

class Config:
    FLASK_APP = 'memo.py'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):    
    FLASK_DEBUG = True

class ProductionConfig(Config):
    FLASK_DEBUG = False

config = {
    'development': DevelopmentConfig, 
    'production': ProductionConfig, 
    'default': Config
}