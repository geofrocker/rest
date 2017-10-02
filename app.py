"""/restful app.py"""
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create User database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
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
# CreateRecipe database model
class Recipe(db.Model):
    __tablename__ = "Recipe"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    ingredients = db.Column(db.String(120), unique=True)
    steps = db.Column(db.String(120), unique=True)
    create_date = db.Column(db.DateTime)

    def __init__(self, id, title, ingredients, steps, create_date):
        self.id = id
        self.title = title
        self.ingredients = ingredients
        self.steps = steps
        self.create_date = create_date


    def __repr__(self):
        return '<Title %r>' % self.title


@app.route('/recipe', methods=['POST'])
def addOne():
    data = request.get_json()
    new_recipe = Recipe(id=str(uuid.uuid4()), title=data['title'], ingredients=data['ingredients'], steps=data['steps'], create_date=data['create_date'])
    db.session.add(new_recipe)
    db.session.commit
    return jsonify({'Message':'Recipe Created'})




if __name__ == '__main__':
    app.run(debug=True)
    