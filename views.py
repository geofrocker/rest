"""/rest api views.py"""
import uuid
from datetime import datetime, timedelta
from flask_restful import reqparse, Resource, marshal
from flask import jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash
from serializer import recipe_serializer, user_serializer
from app import app, api, db
from models import User, Recipe
from decorators import *

class RecipesList(Resource):
    def get(self):
        """
        Get all Recipes
        """
        recipes = Recipe.query.all()
        if recipes:
            recipe_list = marshal(recipes, recipe_serializer)
            return {"Recipe_list": recipe_list}, 200
        else:
            return {'message': 'No recipes found'}, 200
    @token_required
    def post(current_user, self):
        """
        Add a recipe to the database
        """
        data = request.get_json()
        if data:
            new_recipe = Recipe(id=str(uuid.uuid4()), title=data['title'], ingredients=data['ingredients'],
                                steps=data['steps'], create_date=datetime.now(), created_by=data['created_by'],modified_date=datetime.now() )
            db.session.add(new_recipe)
            db.session.commit()
            return {'Message' : 'Recipe Created'}
        return {'Message' : 'Recipe Creation failed'}

api.add_resource(RecipesList, '/')
class RecipeItem(Resource):
    @token_required
    def get(current_user, self,id):
        """get on one recipe"""
        recipe = Recipe.query.filter_by(id=id).first()
        if not recipe:
            return {'Message':'Recipe not found'}
        if recipe:
            recipe_list = marshal(recipe, recipe_serializer)
            return {"Recipe_list": recipe_list}, 200
        else:
            return {'message': 'Recipes Not found'}, 404
    @token_required
    def put(current_user, self, id):
        """Edit a recipe by id"""
        data = request.get_json()
        recipe = Recipe.query.filter_by(id=id).first()
        if not recipe:
            return jsonify({'Message':'Recipe not available'})
        recipe.title = data['title']
        recipe.ingredients = data['ingredients']
        recipe.modified_date = datetime.now()
        recipe.steps = data['steps']
        db.session.commit()
        return {'message':'Recipe Edited successfully'}

    @token_required
    def delete(current_user, self, id):
        """Delete recipe by id"""
        recipe = Recipe.query.filter_by(id=id).first()
        if not recipe:
            return {'Message':'Recipe not available'}
        db.session.delete(recipe)
        db.session.commit()
        return {'message':'Recipe Edited successfully'}

api.add_resource(RecipeItem, '/<id>')

class AuthRegister(Resource):
    def post(self):
        """Register New User"""
        data = request.get_json()
        if data:
            password_hash = generate_password_hash(data['password'], method='sha256')
            new_user = User(id=str(uuid.uuid4()), name=data['name'], username=data['username'],
                            email=data['email'], password=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return {'Message':'User Created'}
        return jsonify({'Message':'No data submitted'})

api.add_resource(AuthRegister, '/auth/register')
class AuthLogin(Resource):
    def post(self):
        """Login a registerd user"""
        auth = request.get_json()
        if not auth or not auth['username'] or not auth['password']:
            return make_response('Could not verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})
        user = User.query.filter_by(username=auth['username']).first()
        if not user:
            return make_response('Could nott verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})

        if check_password_hash(user.password, auth['password']):
            token = jwt.encode({'id' : user.id, 'exp' : datetime.utcnow() + timedelta(minutes=120)}, app.config['SECRET_KEY'])
            return jsonify({'token' : token.decode('UTF-8')})
        return make_response('Could nottt verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})

api.add_resource(AuthLogin, '/auth/login')

class Users(Resource):
    @token_required
    def get(current_user, self):
        """
        get a list of all users
        """
        users = User.query.all()
        if users:
            user_list = marshal(users, user_serializer)
            return {"user_list": user_list}, 200
        else:
            return {'message': 'No users found'}, 404

api.add_resource(Users, '/users')

class OneUser(Resource):
    @token_required
    def get(current_user, self, id):
        """
        Get_one_user
        """
        user = User.query.filter_by(id=id).first()
        if user:
            user_item = marshal(user, user_serializer)
            return {"user_item": user_item}, 200
        else:
            return {'message': 'User not found'}, 404
    
    @token_required
    def delete(current_user, self, id):
        """
        Delete_one_user
        """
        user = User.query.filter_by(id=id).first()
        if not user:
            return {'Message':'User not available'}
        db.session.delete(user)
        db.session.commit()
        return {'Message':'User deleted'}

api.add_resource(OneUser, '/users/<id>')