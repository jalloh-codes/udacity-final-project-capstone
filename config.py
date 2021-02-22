import os
SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True


SQLALCHEMY_TRACK_MODIFICATIONS = False


SQLALCHEMY_DATABASE_URI = 'postgres://hllanhox:gUGLEZB43EJ7YDV0XRV8V9pefd3SyKB1@ziggy.db.elephantsql.com:5432/hllanhox'