"""/rest api app.py"""
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
api = Api(app)
from views import *
if __name__ == '__main__':
    app.run()
    