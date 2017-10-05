"""/rest api models.py"""
from app import db
class User(db.Model):
    """
    Create User database model
    """
    __tablename__ = "User"
    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

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
    title = db.Column(db.String(120))
    ingredients = db.Column(db.String(120))
    steps = db.Column(db.String(120))
    create_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.String, db.ForeignKey('User.id'),nullable=True)

    def __init__(self, id, title, ingredients, steps, create_date, created_by, modified_date):
        self.id = id
        self.title = title
        self.ingredients = ingredients
        self.steps = steps
        self.create_date = create_date
        self.created_by = created_by
        self.modified_date= modified_date

    def __repr__(self):
        return '<Title %r>' % self.title

