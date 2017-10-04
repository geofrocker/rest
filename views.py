"""/rest api views.py"""
import uuid
from datetime import datetime, timedelta
from functools import wraps
from flask_restful import reqparse, Resource, marshal
import jwt
from flask import jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash
from serializer import recipe_serializer
from app import app
from app import api
from models import *


def token_required(f):
    """
    Ensure only logged in users access the system
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'Message': 'You have no access token'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Invalid Token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/recipe/<id>', methods=['GET'])
def get_one_recipe(id):
    """
    Get only one recipe
    """
    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        return jsonify({'Message':'Recipe not found'})
    recipe_data = {}
    recipe_data['id'] = recipe.id
    recipe_data['title'] = recipe.title
    recipe_data['ingredients'] = recipe.ingredients
    recipe_data['steps'] = recipe.steps
    recipe_data['create_date'] = recipe.create_date
    recipe_data['created_by'] = recipe.created_by
    return jsonify({'Recipe':recipe_data})



@app.route('/recipe', methods=['POST'])
def add_one_recipe():
    """
    Add a recipe to the database
    """
    data = request.get_json()
    if data:
        new_recipe = Recipe(id=str(uuid.uuid4()), title=data['title'], ingredients=data['ingredients'],
                            steps=data['steps'], create_date=datetime.now(), created_by=data['created_by'],)
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({'Message' : 'Recipe Created'})
    return jsonify({'Message' : 'Recipe Creation failed'})

@app.route('/recipe/<id>', methods=['PUT'])
def edit_recipe(id):
    """Edit a recipe by id"""
    data = request.get_json()
    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        return jsonify({'Message':'Recipe not available'})
    recipe.title = date['title']
    recipe.ingredients = date['ingredients']
    recipe.steps = date['steps']
    recipe.create_date = date['create_date']
    db.session.commit()
    return jsonify({'message':'User Edited successfully'})

@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    """Delete recipe by id"""
    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        return jsonify({'Message':'Recipe not available'})
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message':'Recipe Edited successfully'})

@app.route('/auth/register', methods=['POST'])
def register_user():
    """
    Register a new user
    """
    data = request.get_json()
    if data:
        password_hash = generate_password_hash(data['password'], method='sha256')
        new_user = User(id=str(uuid.uuid4()), name=data['name'], username=data['username'],
                        email=data['email'], password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'Message':'User Created'})
    return jsonify({'Message':'No data submitted'})
@app.route('/auth/login', methods=['GET'])
def login_user():
    """
    Login a registerd user
    """
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could nott verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.utcnow() + timedelta(seconds=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could nottt verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})

@app.route('/users/<int:page_num>', methods=['GET'])
@token_required
def get_all_users(current_user, page_num):
    """
    get a list of all users
    """
    users = User.query.paginate(per_page=4, page=page_num, error_out=True)
    output = []
    for user in users.items:
        user_info = {}
        user_info['id'] = user.id
        user_info['name'] = user.name
        user_info['username'] = user.username
        user_info['email'] = user.email
        user_info['password'] = user.password

        output.append(user_info)
    return jsonify({'Users':output})

@app.route('/user/<id>', methods=['GET'])
def get_one_user(id):
    """
    Get_one_user
    """
    user = User.query.filter_by(id=id).first()
    user_info = {}
    user_info['id'] = user.id
    user_info['name'] = user.name
    user_info['username'] = user.username
    user_info['email'] = user.email
    user_info['password'] = user.password
    return jsonify({'User' : user_info})

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    """
    Delete_one_user
    """
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'Message':'User not available'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'Message':'User deleted'})

class GetRecipes(Resource):
    def get(self):
        """
        Get all Recipes
        """
        recipes = Recipe.query.paginate()
        if recipes:
            recipe_list = marshal(recipes, recipe_serializer)
            return {"Recipe_list": recipe_list}, 200
        else:
            return {'message': 'No recipes found'}, 404
api.add_resource(GetRecipes, '/')
