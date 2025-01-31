import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config(object):
    SECRET_KEY = 'put secret key here'
    DATABASE = os.path.join(basedir, 'coninfo.db')
