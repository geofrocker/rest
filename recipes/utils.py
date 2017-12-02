"""Handle all the user validation"""
import re

from recipes.models import User, Recipe, Category


def validate_email(email):
    """
    Validate user email
    """
    if len(email) > 7:
        if re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                email) is not None:
            return True
    return False


def validate_text(text):
    """
    Make sure the user does not submit empty strings
    """
    stripped_value = str(text).strip()
    if len(stripped_value) == 0:
        return False
    return True


def clean_recipe(data):
    """
    Ensure that recipe data submitted is clean
    """
    title = data.get('title')
    ingredients = data.get('ingredients')
    steps = data.get('steps')
    status = data.get('status')
    category = data.get('category')
    if not(title and ingredients and steps and status and category):
        return ({'Message': 'Populate all the required fields'}, 400)
    if not validate_text(data['title']):
        return ({'Message': 'Please enter a valid title'}, 400)
    if not validate_text(data['ingredients']):
        return ({'Message': 'Please enter valid ingredients'}, 400)
    if not validate_text(data['steps']):
        return ({'Message': 'Please enter valid steps'}, 400)
    if not(data['status'] == 'public' or data['status'] == 'private'):
        return ({'Message': 'The status should either be public or private'}, 400)
    category = Category.query.filter_by(cat_name=data['category']).first()
    if not category:
        return ({'Message': 'Category does not exist'}, 400)
    recipe_check = Recipe.query.filter_by(title=data['title']).first()
    if recipe_check:
        return ({'Message': 'Title already exists'}, 400)
    return True


def clean_user(data):
    """
    Ensure that user data submitted is clean
    """
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not (name and username and email and password):
        return ({'Message': 'Populate all the fields'}, 400)
    if not validate_email(data['email']):
        return ({'Message': 'Please enter a valid email'}, 400)
    if not len(data['name']) > 3:
        return ({'Message': 'Please enter a valid name'}, 400)
    if not re.match("^[A-Za-z0-9_-]*$", data['username']):
        return ({'Message': 'Please enter a valid Username'}, 400)
    if not len(data['password']) > 4:
        return ({'Message': 'Password must be more than 4 characters'}, 400)
    user_check1 = User.query.filter_by(email=data['email']).first()
    user_check2 = User.query.filter_by(username=data['username']).first()
    if user_check1:
        return ({'Message': 'Email already exists'}, 400)
    if user_check2:
        return ({'Message': 'Username already exists'}, 400)
    return True


def clean_category(data):
    """
    Ensure that category data submitted is clean
    """
    cat_name = data.get('cat_name')
    cat_desc = data.get('cat_desc')
    if not (cat_name and cat_desc):
        return ({'Message': 'Please populate all fields'}, 400)
    if not validate_text(data['cat_name']):
        return ({'Message': 'Please enter a valid category name'}, 400)
    if not validate_text(data['cat_desc']):
        return ({'Message': 'Please enter a valid category description'}, 400)
    category_check = Category.query.filter_by(
        cat_name=data['cat_name']).first()
    if category_check:
        return ({'Message': 'Category name already exists'}, 400)
    return True
