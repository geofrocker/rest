"""/rest app.py"""
import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config


app = Flask(__name__)
CORS(app)
#app.config.from_pyfile('config.py')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['DEBUG'] = config('DEBUG', default=False, cast=bool)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SECRET_KEY'] = config('SECRET_KEY')

db = SQLAlchemy(app)
api = Api(app)
from views import *
if __name__ == '__main__':
    app.run()  
    