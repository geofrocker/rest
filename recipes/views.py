"""/rest_api views.py"""
import uuid
import jwt
import re

from flask import jsonify, make_response, request, redirect, session
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

from flask_restful import Resource, marshal
from decouple import config

from recipes.serializer import recipe_serializer, user_serializer, category_serializer
from recipes import api, db
from recipes.models import User, Recipe, Category
from recipes.models import save, delete
from recipes.utils import validate_email, validate_text

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
            return ({'Message': 'Unauthorised access! Please log in'}, 401)
        try:
            
            data = jwt.decode(token, config('SECRET_KEY'))
            
            current_user = User.query.filter_by(user_id=data['id']).first()
        except:
            return ({'message' : 'Invalid Token'}, 401)
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
            recipes = Recipe.query.filter(Recipe.title.ilike('%' + search + '%'), Recipe.status.ilike('public')).all()
        elif page:
            recipes = Recipe.query.filter_by(status='public').paginate(page, POSTS_PER_PAGE, False)
            pages = recipes.pages
            has_prev = recipes.has_prev
            has_next = recipes.has_next

            if has_next:
                next_page = request.url_root + "?" + \
                        "page=" + str(page + 1)
            else:
                next_page = 'Null'

            if has_prev:
                previous_page = request.url_root + "?" + \
                        "page=" + str(page - 1)
            else:
                previous_page = 'Null'
            recipes = recipes.items
            if recipes:
                recipe_list = marshal(recipes, recipe_serializer)
                return ({"Recipe_list": recipe_list,
                        "has_next": has_next,
                        "total_pages": pages,
                        "previous_page": previous_page,
                        "next_page": next_page
                        }, 200)
            else:
                return ({'message': 'No recipes found'}, 404)

        else:
            recipes = Recipe.query.filter_by(status='public').all()
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
            title = data.get('title')
            ingredients = data.get('ingredients')
            steps = data.get('steps')
            status = data.get('status')
            category = data.get('category')
            if title and ingredients and steps and status and category:
                if validate_text(data['title']):
                    if validate_text(data['ingredients']):
                        if validate_text(data['steps']):
                            if data['status'] == 'public' or data['status'] == 'private':
                                category = Category.query.filter_by(cat_name=data['category']).first()
                                if category:
                                    recipe_check=Recipe.query.filter_by(title=data['title']).first()
                                    if not recipe_check:
                                        new_recipe = Recipe(recipe_id=str(uuid.uuid4()), title=data['title'],
                                                            category=data['category'],
                                                            ingredients=data['ingredients'], steps=data['steps'],
                                                            create_date=datetime.now(),
                                                            created_by=current_user.username, modified_date=datetime.now(), status=data['status'])
                                        save(new_recipe)
                                        return ({'Message' : 'Recipe Created','status':201}, 201)
                                    return ({'Message' : 'Title already exists'}, 400)
                                return ({'Message' : 'Category does not exist'}, 400)
                            return ({'Message' : 'The status should either be public or private'}, 400)
                        return ({'Message' : 'Please enter valid steps'}, 400)
                    return ({'Message' : 'Please enter valid ingredients'}, 400)
                return ({'Message' : 'Please enter a valid title'}, 400)
            return ({'Message' : 'Populate all the required fields'}, 400)
        return ({'Message' : 'No data submitted'}, 400)


class RecipeItem(Resource):
    @token_required
    def get(current_user, self, id):
        """get on one recipe"""
        recipe = Recipe.query.filter_by(recipe_id=id).first()
        if recipe:
            recipe_item = marshal(recipe, recipe_serializer)
            return {"Recipe_Item": recipe_item}, 200
        else:
            return {'message': 'Recipe Not found'}, 404
    @token_required
    def put(current_user, self, id):
        """Edit a recipe by id"""
        data = request.get_json()
        recipe = Recipe.query.filter_by(recipe_id=id).first()
        if not recipe:
            return ({'Message':'Recipe not available'}, 404)
        if data:
            title = data.get('title')
            ingredients = data.get('ingredients')
            steps = data.get('steps')
            status = data.get('status')
            category = data.get('category')
            if title and ingredients and steps and status and category:
                if validate_text(data['title']):
                    if validate_text(data['ingredients']):
                        if validate_text(data['steps']):
                            if data['status'] == 'public' or data['status'] == 'private':
                                category = Category.query.filter_by(cat_name=data['category']).first()
                                if category:
                                    recipe_check=Recipe.query.filter_by(title=data['title']).first()
                                    if not recipe_check:
                                        recipe.title = data['title']
                                        recipe.category = data['category']
                                        recipe.ingredients = data['ingredients']
                                        recipe.modified_date = datetime.now()
                                        recipe.steps = data['steps']
                                        recipe.status = data['status']
                                        db.session.commit()
                                        return ({'Message':'Recipe Edited successfully','status':201}, 201)
                                    return ({'Message' : 'Title already exists'}, 400)
                                return ({'Message' : 'Category does not exist'}, 400)
                            return ({'Message' : 'The status should either be public or private'}, 400)
                        return ({'Message' : 'Please enter valid steps'}, 400)
                    return ({'Message' : 'Please enter valid ingredients'}, 400)
                return ({'Message' : 'Please enter a valid title'}, 400)
            return ({'Message' : 'Populate all the required fields'}, 400)
        return ({'Message' : 'No data submitted'}, 400)

    @token_required
    def delete(current_user, self, id):
        """Delete recipe by id"""
        recipe = Recipe.query.filter_by(recipe_id=id).first()
        if not recipe:
            return ({'Message':'Recipe not available'}, 404)
        delete(recipe)
        return redirect("/myrecipes")
        return ({'message':'Recipe Deleted successfully'}, 200)



class AuthRegister(Resource):
    def post(self):
        """Register New User"""
        data = request.get_json()
        if data:
            name = data.get('name')
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            if name and username and email and password:
                if validate_email(data['email']):
                    if len(data['name']) > 3:
                        if re.match("^[A-Za-z0-9_-]*$", data['username']):
                            if len(data['password']) > 4:
                                user_ckeck1 = User.query.filter_by(email=data['email']).first()
                                user_ckeck2 = User.query.filter_by(username=data['username']).first()
                                if not user_ckeck1:
                                    if not user_ckeck2:
                                        password_hash = generate_password_hash(data['password'], method='sha256')
                                        new_user = User(user_id=str(uuid.uuid4()), name=data['name'], username=data['username'],
                                                        email=data['email'], password=password_hash)
                                        save(new_user)
                                        return ({'Message':'Your are now registered! You can log in','status':201}, 201)
                                    return ({'Message':'Username already exists'}, 200)
                                return ({'Message':'Email already exists'}, 200)
                            return ({'Message':'Password must be more than 4 characters'}, 200)
                        return ({'Message':'Please enter a valid Username'}, 200)
                    return ({'Message':'Please enter a valid name'}, 200)
                return ({'Message':'Please enter a valid email'}, 200)
            return ({'Message':'Populate all the fields'}, 200)
        return ({'Message':'No data submitted'}, 200)


class AuthLogin(Resource):
    def post(self):
        """Login a registerd user"""
        auth = request.get_json()
        if not auth or not auth['username'] or not auth['password']:
            return make_response(jsonify(dict(error='Please enter your username and password')), 401)
        user = User.query.filter_by(username=auth['username']).first()
        if not user:
            return make_response(jsonify(dict(error='User does not exist')), 401)

        if check_password_hash(user.password, auth['password']):
            token = jwt.encode({'id' : user.user_id, 'exp' : datetime.utcnow() + timedelta(minutes=6000)}, config('SECRET_KEY'))
            return jsonify({'token' : token.decode('UTF-8')})
        return make_response(jsonify(dict(error='Invalid password')), 401)



class Users(Resource):
    @token_required
    def get(current_user, self):
        """
        get a list of all users
        """
        users = User.query.all()
        if users:
            user_list = marshal(users, user_serializer)
            return ({"user_list": user_list}, 200)
        else:
            return ({'message': 'No users found'}, 404)


class OneUser(Resource):
    @token_required
    def get(current_user, self, id):
        """
        Get_one_user
        """
        user = User.query.filter_by(user_id=id).first()
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
        user = User.query.filter_by(user_id=id).first()
        if not user:
            return ({'Message':'User not available'}, 404)
        connected_recipes = Recipe.query.filter_by(created_by=user.username).first()
        if not connected_recipes:
            delete(user)
            return ({'Message':'User deleted'}, 200)
        return ({'message': 'There are recipes attached to this user! Deletion failed'}, 401)

class CategoryList(Resource):
    
    def get(self):
        """
        Get all Categories
        """
        categories = Category.query.all()
        if categories:
            category_list = marshal(categories, category_serializer)
            return ({"Category_list": category_list}, 200)
        else:
            return ({'message': 'No categories found'}, 404)
    @token_required
    def post(current_user, self):
        """
        Add a category to the database
        """
        data = request.get_json()
        if data:
            cat_name = data.get('cat_name')
            cat_desc = data.get('cat_desc')
            if cat_name and cat_desc:
                if validate_text(data['cat_name']):
                    if validate_text(data['cat_desc']):
                        category_check = Category.query.filter_by(cat_name=data['cat_name'], created_by=current_user.username).first()
                        if not category_check:
                            new_category = Category(cat_id=str(uuid.uuid4()), cat_name=data['cat_name'],
                                                    cat_desc=data['cat_desc'], create_date=datetime.now(),
                                                    created_by=current_user.username, modified_date=datetime.now())
                            save(new_category)
                            return ({'Message' : 'Category Created','status':201}, 201)
                        return ({'Message' : 'Category name already exists'}, 400)
                    return ({'Message' : 'Please enter a valid category description'}, 400)
                return ({'Message' : 'Please enter a valid category name'}, 400)
            return ({'Message' : 'Please populate all fields'}, 400)
        return ({'Message' : 'No data submitted'}, 400)


class CategoryItem(Resource):
    @token_required
    def get(current_user, self, id):
        """get one category"""
        category = Category.query.filter_by(cat_id=id).first()
        if category:
            category_item = marshal(category, category_serializer)
            return ({"Category_Item": category_item}, 200)
        else:
            return ({'message': 'Category Not found'}, 404)
    @token_required
    def put(current_user, self, id):
        """Edit a Category by id"""
        data = request.get_json()
        category = Category.query.filter_by(cat_id=id).first()
        if not category:
            return ({'message': 'Category Not found'}, 404)
        if data:
            cat_name = data.get('cat_name')
            cat_desc = data.get('cat_desc')
            if cat_name and cat_desc:
                if validate_text(data['cat_name']):
                    if validate_text(data['cat_desc']):
                        connected_recipes = Recipe.query.filter_by(category=category.cat_name).first()
                        if not connected_recipes:
                            category_check = Category.query.filter_by(cat_name=data['cat_name'], created_by=current_user.username).first()
                            if not category_check:
                                category.cat_name = data['cat_name']
                                category.cat_desc = data['cat_desc']
                                category.modified_date = datetime.now()
                                db.session.commit()
                                return ({'message':'Category Edited successfully','status':201}, 201)
                            return ({'Message' : 'Category name already exists'}, 400)
                        return ({'Message' : 'Cannot edit recipe because there a recipes attached to it'}, 400)
                    return ({'Message' : 'Please enter a valid category description'}, 400)
                return ({'Message' : 'Please enter a valid category name'}, 400)
            return ({'Message' : 'Please populate all fields'}, 400)
        return ({'Message' : 'No data submitted'}, 400)

    @token_required
    def delete(current_user, self, id):
        """Delete Category by id"""
        category = Category.query.filter_by(cat_id=id).first()
        if not category:
            return ({'message': 'Category Not found'}, 404)
        connected_recipes = Recipe.query.filter_by(category=category.cat_name).first()
        if not connected_recipes:
            delete(category)
            return ({'message':'Category Deleted successfully'}, 200)
        return ({'message':'Category has recipes attached to it. Deletion failed'}, 401)

class MyRecipes(Resource):
    @token_required
    def get(current_user, self, page=1):
        """
        Get all Recipes
        """
        recipes = Recipe.query.filter_by(created_by=current_user.username).all()
        if recipes:
            recipe_list = marshal(recipes, recipe_serializer)
            return ({"Recipe_list": recipe_list}, 200)
        else:
            return ({'message': 'No recipes found'}, 404)

class Upvote(Resource):
    @token_required
    def get(current_user, self, id):
        recipe = Recipe.query.filter_by(recipe_id=id).first()
        if not session.get('voted') and not session.get('voted_user') == id:
            recipe.upvotes = recipe.upvotes + 1
            db.session.commit()
            session['voted'] = True
            session['voted_recipe'] = id
            return redirect("/"+id)
        return ({'message': 'You have already voted'}, 404)
        


class Documentation(Resource):
    def get(self):
        return redirect("https://app.swaggerhub.com/apis/Geeks4lif/YummyRecipesRet/1.0.0#/")

api.add_resource(Upvote, '/recipe/upvote/<id>')
api.add_resource(MyRecipes, '/myrecipes')
api.add_resource(RecipesList, '/')
api.add_resource(RecipeItem, '/<id>')
api.add_resource(AuthRegister, '/auth/register')
api.add_resource(AuthLogin, '/auth/login')
api.add_resource(Users, '/users')
api.add_resource(OneUser, '/users/<id>')
api.add_resource(CategoryList, '/category')
api.add_resource(CategoryItem, '/category/<id>')
api.add_resource(Documentation, '/documentation')
