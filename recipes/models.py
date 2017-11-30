"""/rest_api models.py"""
from recipes import db
class User(db.Model):
    """
    Create User database model
    """
    __tablename__ = "User"
    user_id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '%r' % self.recipe_id

# Create Recipe database model
class Recipe(db.Model):
    __tablename__ = "Recipe"
    recipe_id = db.Column(db.String(120), primary_key=True)
    title = db.Column(db.String(120))
    category = db.Column(db.String, db.ForeignKey('Category.cat_name'), nullable=True)
    ingredients = db.Column(db.String(120))
    steps = db.Column(db.String(120))
    create_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.String, db.ForeignKey('User.username'), nullable=True)
    status = db.Column(db.String, default='public')
    upvotes = db.Column(db.Integer, default=0)
    reviews = db.relationship("Review", backref='recipe', lazy='dynamic',
                              cascade="delete, delete-orphan")
    

    def __repr__(self):
        return '%r' % self.title

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

# Create review model
class Review(db.Model):
    __tablename__ = "Review"
    review_id = db.Column(db.String(120), primary_key=True)
    content = db.Column(db.String(120))
    recipe_id = db.Column(db.String, db.ForeignKey('Recipe.recipe_id'), nullable=True)
    create_date = db.Column(db.DateTime)
    created_by = db.Column(db.String, db.ForeignKey('User.username'), nullable=True)

    def __repr__(self):
        return '%r' % self.content

def save(model_instance):
    """
    method used for adding categories
    """
    db.session.add(model_instance)
    db.session.commit()

def delete(model_instance):
    """
    method used for deleting categories
    """
    db.session.delete(model_instance)
    db.session.commit()
