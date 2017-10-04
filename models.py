"""/rest api models.py"""
from app import db
class User(db.Model):
    """
    Create User database model
    """
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
    created_by = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)

    def __init__(self, id, title, ingredients, steps, create_date, created_by):
        self.id = id
        self.title = title
        self.ingredients = ingredients
        self.steps = steps
        self.create_date = create_date
        self.created_by = created_by

    def __repr__(self):
        return '<Title %r>' % self.title