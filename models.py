"""/rest_api models.py"""
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
    category = db.Column(db.String, db.ForeignKey('Category.cat_name'), nullable=True)
    ingredients = db.Column(db.String(120))
    steps = db.Column(db.String(120))
    create_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.String, db.ForeignKey('User.username'), nullable=True)

    def __init__(self, id, title, category, ingredients, steps, create_date, created_by, modified_date):
        self.id = id
        self.title = title
        self.ingredients = ingredients
        self.steps = steps
        self.create_date = create_date
        self.created_by = created_by
        self.modified_date= modified_date

    def __repr__(self):
        return '<Title %r>' % self.title

class Category(db.Model):
    __tablename__ = "Category"
    cat_id = db.Column(db.String(100), primary_key=True)
    cat_name = db.Column(db.String(50), unique=True)
    cat_desc = db.Column(db.String(100))
    create_date = db.Column(db.DateTime)
    created_by = db.Column(db.String, db.ForeignKey('User.username'), nullable=True)
    modified_date = db.Column(db.DateTime)

    def __init__(self, cat_id, cat_name, cat_desc, create_date, created_by, modified_date):
        self.cat_id = cat_id
        self.cat_name = cat_name
        self.cat_desc = cat_desc
        self.create_date = create_date
        self.created_by = created_by
        self.modified_date = modified_date
        
    def __repr__(self):
        return '<Name %r>' % self.cat_name

