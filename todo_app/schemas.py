from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from models import Task

ma = Marshmallow()

class Post_GetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task  #read about model binding in 'class_Meta.txt' in notes folder.
        load_instance = True

class PatchSchema(Schema): #this should make a dictionary
    Title = fields.Str(required=False)
    Status = fields.Bool(required=False)

class PutSchema(Schema):  #this should make a dictionary. schema made from SQLAlchemyAutoSchema will directly make db objects
    Title = fields.Str(required=True)   #when their load method is called.
    Status = fields.Bool(required=True)