import os

PROJECT = "webapp"

# Get app root path, also can use flask.root_path
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
TESTING = False

ADMINS = ['judyzhangyifan@gmail.com']

# http://flask.pocoo.org/docs/quickstart/#sessions
SECRET_KEY = 'youshouldreplacethis'

SQLALCHEMY_ECHO = True
DATABASE_QUERY_TIMEOUT = 15
# Database URI to connect to the implied local mySQL server.
# Needs to be changed if you want to deploy on your local machine for testing
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://capstone2021:capstone2021@127.0.0.1:3306/spam_detection_survey'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///spamSpottingData.db'

# Mailto dev configs
MAIL_DEBUG = DEBUG
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'yiz222'
MAIL_PASSWORD = 'mpwn davr vkdn ofqe'
DEFAULT_MAIL_SENDER = '%s@lehigh.edu' % MAIL_USERNAME
