"""/rest_api models.py"""
from recipes import db
class User(db.Model):
    """
    Create User database model
    """
    __tablename__ = "User"
    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '%r' % self.id

    def save(self):
        """
        method used for adding users
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        method used for deleting users
        """
        db.session.delete(self)
        db.session.commit()

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
        return '%r' % self.title

    def save(self):
        """
        method used for adding recipes
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        method used for deleting recipes
        """
        db.session.delete(self)
        db.session.commit()

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

    def save(self):
        """
        method used for adding categories
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        method used for deleting categories
        """
        db.session.delete(self)
        db.session.commit()
