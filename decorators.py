from flask import request
import jwt
from functools import wraps
from models import User
from app import app

def token_required(f):
    """
    Ensure only logged in users access the system
    """
    @wraps(f)
    def decorated(*args, **kwargs):
 
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'Message': 'You have no access token'}, 401
        try:
            
            data = jwt.decode(token, app.config['SECRET_KEY'])
            
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return {'message' : 'Invalid Token'}, 401
        return f(current_user, *args, **kwargs)
    return decorated