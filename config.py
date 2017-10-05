"""/Rest api config.py"""
import os
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:elizei2@127.0.0.1:5432/rest_api'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)
    