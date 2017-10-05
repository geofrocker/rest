from flask_restful import fields

recipe_serializer = {
    "id": fields.String,
    "title": fields.String,
    "steps": fields.String,
    "ingredients": fields.String,
    "steps": fields.String,
    "create_date": fields.DateTime,
    "created_by": fields.String,
    "modified_date": fields.DateTime,
    
   
}

user_serializer = {
    "id": fields.String,
    "name": fields.String,
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
   
}