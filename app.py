"""/rest api app.py"""
from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create User database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)

    def __init__(self, id, name, username, email, password):
        self.id = id
        self.name = email
        self.username = username
        self.email = email
        self.password = password
        


    def __repr__(self):
        return '<Username %r>' % self.username
# Create Recipe database model
class Recipe(db.Model):
    __tablename__ = "Recipe"
    id = db.Column(db.String(120), primary_key=True)
    title = db.Column(db.String(120), unique=True)
    ingredients = db.Column(db.String(120), unique=True)
    steps = db.Column(db.String(120), unique=True)
    create_date = db.Column(db.DateTime)
    created_by = db.Column(db.Integer)

    def __init__(self, id, title, ingredients, steps, create_date, created_by):
        self.id = id
        self.title = title
        self.ingredients = ingredients
        self.steps = steps
        self.create_date = create_date
        self.created_by = created_by

    def __repr__(self):
        return '<Title %r>' % self.title

def token_required(f):
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

        

@app.route('/', methods=['GET'])
def get_all():
    recipes = Recipe.query.all()
    output = []
    for recipe in recipes:
        recipe_data = {}
        recipe_data['id'] = recipe.id
        recipe_data['title'] = recipe.title
        recipe_data['ingredients'] = recipe.ingredients
        recipe_data['steps'] = recipe.steps
        recipe_data['create_date'] = recipe.create_date
        recipe_data['created_by'] = recipe.created_by
        output.append(recipe_data)
    return jsonify({'Recipes':output})


@app.route('/recipe/<id>', methods=['GET'])
def get_one_recipe(id):
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
    data = request.get_json()
    if data:
        new_recipe = Recipe(id=str(uuid.uuid4()), title=data['title'], ingredients=data['ingredients'],
                            steps=data['steps'], create_date=datetime.now(), created_by=data['created_by'],)
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({'Message':'Recipe Created'})
    return jsonify({'Message':'Recipe Creation failed'})

@app.route('/recipe/<id>', methods=['PUT'])
def edit_recipe(id):
    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        return jsonify({'Message':'Recipe not available'})
    recipe.title ="Dummy Edit"
    db.session.commit()
    return jsonify({'message':'User Edited successfully'})

@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        return jsonify({'Message':'Recipe not available'})
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message':'Recipe Edited successfully'})

@app.route('/auth/register', methods=['POST'])
def register_user():
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
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify user', 401, {'WWW-Authenticate' : 'Basic Realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)
    