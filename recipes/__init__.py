import os, sys
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config


app = Flask(__name__)
CORS(app)
#app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL') or os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['DEBUG'] = config('DEBUG', default=False, cast=bool)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config('SECRET_KEY') or os.environ['SECRET_KEY']

db = SQLAlchemy(app)
api = Api(app)
from recipes import views