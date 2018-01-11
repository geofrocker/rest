"""Handle all the user validation"""
import re

from app.models import User, Recipe, Category


def validate_email(email):
    """
    Validate user email
    """
    if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",email) is not None:
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

def text_to_title_case(text):
    """
    Covert data to title case
    """
    new = ' '.join(''.join([w[0].upper(), w[1:].lower()]) for w in text.split())
    return new


def clean_recipe(data):
    """
    Ensure that recipe data submitted is clean
    """
    title = data.get('title')
    ingredients = data.get('ingredients')
    steps = data.get('steps')
    status = data.get('status')
    category = data.get('category')
    category = text_to_title_case(category)
    msg = ''
    if not(title and ingredients and steps and status):
        msg = msg + 'Populate all the required fields, '
        return ({'Message': msg}, 400)
    if not(category):
        msg = msg + 'Add atleast one category before creating a recipe, '
        return ({'Message': msg}, 400)
    if not validate_text(title):
        msg = msg + 'Please enter a valid title, '
    if not validate_text(ingredients):
        msg = msg + 'Please enter valid ingredients, '
    if not validate_text(steps):
        msg = msg + 'Please enter valid steps, '
    if not(status == 'public' or status == 'private'):
        msg = msg + 'The status should either be public or private, '
    category = Category.query.filter_by(cat_name=category).first()
    if not category:
        msg = msg + 'Category does not exist, '
    title = text_to_title_case(title)
    recipe_check = Recipe.query.filter_by(title=title).first()
    if recipe_check:
        msg = msg + 'Title already exists, '
    if msg:
        return ({'Message': msg}, 400)
    return True


def clean_user(data):
    """
    Ensure that user data submitted is clean
    """
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    msg = ''
    if not (name and username and email and password):
        msg = msg + 'Populate all the fields, '
    if isinstance(name, int) or isinstance(username, int) or isinstance(email, int) or isinstance(password, int):
        msg = msg + 'Check your fields for integers, '
        return ({'Message': msg}, 400)
    if not validate_email(email):
        msg = msg + 'Please enter a valid email, '
    if not len(name) > 3:
        msg = msg + 'Please enter a valid name, '
    if not re.match("^[A-Za-z0-9_-]*$", username):
        msg = msg + 'Please enter a valid Username, '
    if not len(password) > 4:
        msg = msg + 'Password must be more than 4 characters, '
    user_check1 = User.query.filter_by(email=email).first()
    username = text_to_title_case(username)
    user_check2 = User.query.filter_by(username=username).first()
    if user_check1:
        msg = msg + 'Email already exists, '
    if user_check2:
        msg = msg + 'Username already exists, '
    if msg:
        return ({'Message': msg}, 400)
    return True


def clean_category(data):
    """
    Ensure that category data submitted is clean
    """
    cat_name = data.get('cat_name')
    cat_desc = data.get('cat_desc')
    msg = ''
    if not (cat_name and cat_desc):
        msg = msg + 'Please populate all fields, '
        return ({'Message': msg}, 400)
    if not validate_text(cat_name):
        msg = msg + 'Please enter a valid category name, '
    if not validate_text(cat_desc):
        msg = msg + 'Please enter a valid category description, '
    cat_name = ' '.join(''.join([w[0].upper(), w[1:].lower()]) for w in cat_name.split()),
    category_check = Category.query.filter_by(
        cat_name=cat_name).first()
    if category_check:
        msg = msg + 'Category name already exists, '
    if msg:
        return ({'Message': msg}, 400)
    return True
