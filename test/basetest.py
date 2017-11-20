"""/rest_api basetest.py"""
import os
from flask import Flask, request
from unittest import TestCase
from recipes import app, db
from recipes.models import User, Recipe, Category
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
from decouple import config
import json

class BaseTestCase(TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/ApiTests'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()
        
        # create and add a test user        
        password = '12345'
        self.user_test={'id':'5xxxxx', 'name':'Geofrey', 'username':'geof', 'email':'geom@gmail.com', 'password':password}
        password_hash = generate_password_hash(password, method='sha256')
        test_user = User(id='5xxxxx', name='Geofrey', username='geom', email='geom@gmail.com', password=password_hash)
        db.session.add(test_user)
        db.session.commit()

        # create and add test category
        self.cat_test={'cat_id':'5xxxxxx','cat_name':'Generall','cat_desc':'General recpes','created_by':None}
        test_category = Category(cat_id='5xxxxx', cat_name='General', cat_desc='General recpes', create_date=datetime.now(), created_by=None, modified_date=datetime.now())
        db.session.add(test_category)
        db.session.commit()

        # create and add test recipe
        self.recipe_test={'id':'5xxxxx','title':'Recipe One','category':None,'ingredients':'Ingredient one and two','steps':'step 1','created_by':None}
        test_recipe = Recipe(id='5xxxxx', title='Recipe One', category=None, ingredients='Ingredient one and two', steps='step 1', create_date=datetime.now(), created_by=None, modified_date=datetime.now())
        db.session.add(test_recipe)
        db.session.commit()

        """ Generate authentication token"""
        self.user = {"username": "geom", "password": password}
        response = self.client.post(
            '/auth/login', data=json.dumps(self.user),
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