"""BaseTestCase"""
from flask import Flask, request
from unittest import TestCase
from app import app, db, User, Recipe
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
        """ Generate authentication token"""
        self.user_login = {"username": "geom", "password": password}
        response = self.client.post(
            '/auth/login', data=self.user_login,
            headers={'Content-Type': 'application/json'})
        import pdb; pdb.set_trace()
        response_data = json.loads(response.data)
        
        token = response_data['Token']
        self.headers = {'Authorization': token,
                        'Content-Type': 'application/json',
                        }
        
    def tearDown(self):
        db.drop_all()
