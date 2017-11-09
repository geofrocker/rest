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
        
    def __repr__(self):
        return '<Name %r>' % self.cat_name
