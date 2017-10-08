"""BaseTestCase"""
from flask import Flask, request
from unittest import TestCase
from app import app, db
from models import User, Recipe
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
import json

class BaseTestCase(TestCase):
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:elizei2@127.0.0.1:5432/ApiTests'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()
        
        # create and add a test user        
        password = '12345'
        self.user_test={'id':'5xxxxx', 'name':'Geofrey', 'username':'geom', 'email':'geom@gmail.com', 'password':password}
        password_hash = generate_password_hash(password, method='sha256')
        test_user = User(id='5xxxxx', name='Geofrey', username='geom', email='geom@gmail.com', password=password_hash)
        db.session.add(test_user)
        db.session.commit()

        # create and add test recipe
        self.recipe_test={'id':'5xxxxx','title':'Recipe One','ingredients':'Ingredient one and two','steps':'step 1','created_by':None}
        test_recipe = Recipe(id='5xxxxx', title='Recipe One', ingredients='Ingredient one and two', steps='step 1', create_date=datetime.now(), created_by=None, modified_date=datetime.now())
        db.session.add(test_recipe)
        db.session.commit()

        """ Generate authentication token"""
        user = {"username": "geom", "password": password}
        response = self.client.post(
            '/auth/login', data=json.dumps(user),
            headers={'Content-Type': 'application/json'})
        
        response_data = json.loads(response.data)
        token = response_data['token']

        self.headers = {'x-access-token': token,
                        'Content-Type': 'application/json',
                        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == "__main__":
    unittest.main()