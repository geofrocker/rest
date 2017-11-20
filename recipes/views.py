"""/rest_api views.py"""
import uuid
from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask_restful import Resource, marshal
from flask import jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash
from recipes.serializer import recipe_serializer, user_serializer, category_serializer
from recipes import api, db
from recipes.models import User, Recipe, Category
from decouple import config
POSTS_PER_PAGE = 1

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
            return {'Message': 'You have no access token'}, 401
        try:
            
            data = jwt.decode(token, config('SECRET_KEY'))
            
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return {'message' : 'Invalid Token'}, 401
        return f(current_user, *args, **kwargs)
    return decorated


class RecipesList(Resource):
    def get(self):
        """
        Get all Recipes
        """
        search = request.args.get('q')
        page = request.args.get('page')
        if page:
            page = int(page)
        if search:
            recipes = Recipe.query.filter(Recipe.title.ilike('%' + search + '%')).paginate(page, 1, False).items
        elif page:
            recipes = Recipe.query.paginate(page, POSTS_PER_PAGE, False).items
        else:
            recipes = Recipe.query.all()
        if recipes:
            recipe_list = marshal(recipes, recipe_serializer)
            return ({"Recipe_list": recipe_list}, 200)
        else:
            return ({'message': 'No recipes found'}, 404)

    @token_required
    def post(current_user, self):
        """
        Add a recipe to the database
        """
        data = request.get_json()
        if data:
            new_recipe = Recipe(id=str(uuid.uuid4()), title=data['title'],
                                category=data['category'],
                                ingredients=data['ingredients'], steps=data['steps'],
                                create_date=datetime.now(),
                                created_by=current_user.username, modified_date=datetime.now())
            db.session.add(new_recipe)
            db.session.commit()
            return ({'Message' : 'Recipe Created'}, 201)
        return ({'Message' : 'Recipe Creation failed'}, 200)


class RecipeItem(Resource):
    @token_required
    def get(current_user, self, id):
        """get on one recipe"""
        recipe = Recipe.query.filter_by(id=id).first()
        if recipe:
            recipe_item = marshal(recipe, recipe_serializer)
            return {"Recipe_Item": recipe_item}, 200
        else:
            return {'message': 'Recipe Not found'}, 404
    @token_required
    def put(current_user, self, id):
        """Edit a recipe by id"""
        data = request.get_json()
        recipe = Recipe.query.filter_by(id=id).first()
        if not recipe:
            return ({'Message':'Recipe not available'}, 404)
        recipe.title = data['title']
        recipe.category = data['category']
        recipe.ingredients = data['ingredients']
        recipe.modified_date = datetime.now()
        recipe.steps = data['steps']
        db.session.commit()
        return ({'message':'Recipe Edited successfully'}, 201)

    @token_required
    def delete(current_user, self, id):
        """Delete recipe by id"""
        recipe = Recipe.query.filter_by(id=id).first()
        if not recipe:
            return ({'Message':'Recipe not available'}, 404)
        db.session.delete(recipe)
        db.session.commit()
        return ({'message':'Recipe Deleted successfully'}, 200)



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
            return ({'Message':'User Created'}, 201)
        return ({'Message':'No data submitted'}, 200)


class AuthLogin(Resource):
    def post(self):
        """Login a registerd user"""
        auth = request.get_json()
        if not auth or not auth['username'] or not auth['password']:
            return make_response('Could not verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})
        user = User.query.filter_by(username=auth['username']).first()
        if not user:
            return make_response('Invalid user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})

        if check_password_hash(user.password, auth['password']):
            token = jwt.encode({'id' : user.id, 'exp' : datetime.utcnow() + timedelta(minutes=60)}, config('SECRET_KEY'))
            return jsonify({'token' : token.decode('UTF-8')})
        return make_response('Invalid password', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})



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


class OneUser(Resource):
    @token_required
    def get(current_user, self, id):
        """
        Get_one_user
        """
        user = User.query.filter_by(id=id).first()
        if user:
            user_item = marshal(user, user_serializer)
            return ({"user_item": user_item}, 200)
        else:
            return ({'message': 'User not found'}, 404)
    
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


class CategoryList(Resource):
    def get(self):
        """
        Get all Categories
        """
        categories = Category.query.all()
        if categories:
            category_list = marshal(categories, category_serializer)
            return {"Category_list": category_list}, 200
        else:
            return {'message': 'No categories found'}, 404

    def post(self):
        """
        Add a category to the database
        """
        data = request.get_json()
        if data:
            new_category = Category(cat_id=str(uuid.uuid4()), cat_name=data['cat_name'],
                                    cat_desc=data['cat_desc'], create_date=datetime.now(),
                                    created_by=data['created_by'], modified_date=datetime.now())
            db.session.add(new_category)
            db.session.commit()
            return {'Message' : 'Category Created'}
        return {'Message' : 'Category  Creation failed'}


class CategoryItem(Resource):
    @token_required
    def get(current_user, self, id):
        """get one category"""
        category = Category.query.filter_by(cat_id=id).first()
        if not category:
            return {'Message':'Category not found'}
        if category:
            category_item = marshal(category, category_serializer)
            return {"Category_Item": category_item}, 200
        else:
            return {'message': 'Category Not found'}, 404
    @token_required
    def put(current_user, self, id):
        """Edit a Category by id"""
        data = request.get_json()
        category = Category.query.filter_by(cat_id=id).first()
        if not category:
            return jsonify({'Message':'Category not available'})
        category.cat_name = data['cat_name']
        category.cat_desc = data['cat_desc']
        category.modified_date = datetime.now()
        db.session.commit()
        return {'message':'Category Edited successfully'}

    @token_required
    def delete(current_user, self, id):
        """Delete Category by id"""
        category = Category.query.filter_by(cat_id=id).first()
        if not category:
            return {'Message':'Category not available'}
        db.session.delete(category)
        db.session.commit()
        return {'message':'Category Deleted successfully'}



class Dashboard(Resource):
    @token_required
    def get(current_user, self, page=1):
        """
        Get all Recipes
        """
        search = request.args.get('q')
        if search:
            recipes = Recipe.query.filter_by(created_by=current_user.username).filter(Recipe.title.ilike('%' + search + '%')).paginate(page, POSTS_PER_PAGE, False).items
            if recipes:
                recipe_list = marshal(recipes, recipe_serializer)
                return {"Recipe_list": recipe_list}, 200
            else:
                return {'message': 'No recipes found'}, 404

        recipes = Recipe.query.filter_by(created_by=current_user.username).paginate(page, POSTS_PER_PAGE, False).items
        if recipes:
            recipe_list = marshal(recipes, recipe_serializer)
            return {"Recipe_list": recipe_list}, 200
        else:
            return {'message': 'No recipes found'}, 404

api.add_resource(Dashboard, '/dashboard')
api.add_resource(RecipesList, '/')
api.add_resource(RecipeItem, '/<id>')
api.add_resource(AuthRegister, '/auth/register')
api.add_resource(AuthLogin, '/auth/login')
api.add_resource(Users, '/users')
api.add_resource(OneUser, '/users/<id>')
api.add_resource(CategoryList, '/category')
api.add_resource(CategoryItem, '/category/<id>')
