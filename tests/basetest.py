"""BaseTestCase"""
from flask import Flask, request
from unittest import TestCase
from app import app, db
from models import User, Recipe
from flask_sqlalchemy import SQLAlchemy
import json

class BaseTestCase(TestCase):
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:elizei2@127.0.0.1:5432/ApiTests'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    def setUp(self):
        self.client = app.test_client()
        db.init_app(app)
        db.create_all()
        password = '12345'
        self.user={'id':'5xxxxx', 'name':'Geofrey', 'username':'geom', 'email':'geom@gmail.com', 'password':password}
        #self.user=User(id='5xxxxx', name='Geofrey', username='geom', email='geom@gmail.com', password='12345')
        #db.session.add(self.user)
        #db.session.commit()
        
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjM4NDM5NGYyLTcxZWYtNDZhOS1iOGQ1LWE5MWI4Yjk4MmMwZiIsImV4cCI6MTUwNzI1NDUwNX0.DnsMeUsIGK2hab4oXb4DRqegfhtB9osi0VF7UoAXErg'
        headers = {'Authorization': 'Basic eyJ0eXAiOiJKV1QiLCJhb',
                                'Content-Type': 'application/json',
                                'x-access-token' : token
                                }
        
    def tearDown(self):
        db.drop_all()
