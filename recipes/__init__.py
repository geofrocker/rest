import os, sys
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config


app = Flask(__name__)
CORS(app)
#app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['DEBUG'] = config('DEBUG', default=False, cast=bool)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

db = SQLAlchemy(app)
api = Api(app)
from recipes import views