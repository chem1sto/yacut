import os
from string import ascii_letters, digits

API_ORIGINAL = 'url'
API_SHORT = 'short_link'
ALPHABET = ascii_letters + digits
ORIGINAL = 'original_link'
SHORT = 'custom_id'
DEFAULT_APP = 'yacut'
DEFAULT_ENV = 'development'
DEFAULT_SECRET_KEY = '123456'
DEFAULT_DATABASE = 'sqlite:///db.sqlite3'
DEFAULT_PORT = 5000
LINK_SIZE_MIN = 10
MAIN_PAGE = 'index.html'
NO_URL_ERROR_MESSAGE = '"url" является обязательным полем!'
PATTERN = rf'^[{ALPHABET}]*$'
PORT = os.getenv('PORT', DEFAULT_PORT)
REPEAT = 20
REDIRECTION_VIEW = 'redirection_view'
SHORT_AUTO_LENGTH = 6
SHORT_MAX_LENGTH = 16


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', DEFAULT_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', DEFAULT_SECRET_KEY)
