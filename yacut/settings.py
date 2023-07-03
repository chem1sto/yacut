import os


API_ORIGINAL = 'url'
API_SHORT = 'custom_id'
BASE_URL = f'http://{os.getenv("HOST", "localhost")}'
CUSTOM_ID_AUTO_LENGTH = 6
CUSTOM_ID_MAX_LENGTH = 16
DEFAULT_APP = 'yacut'
DEFAULT_ENV = 'development'
DEFAULT_SECRET_KEY = '123456'
DEFAULT_DATABASE = 'sqlite:///db.sqlite3'
DEFAULT_PORT = 5000
LINK_SIZE_MAX = 256
LINK_SIZE_MIN = 10
MAIN_PAGE = 'index.html'
PATTERN = r'[a-zA-Z0-9]'
PORT = os.getenv('PORT', DEFAULT_PORT)


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', DEFAULT_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', DEFAULT_SECRET_KEY)
