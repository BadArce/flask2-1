from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from sqlalchemy_work import db
import uuid
from datetime import datetime
from db import db

class AppUsers(db.Model):
  __tablename__ = "Users"
  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid)
  first_name= db.Column(db.String(), nullable=False)
  last_name= db.Column(db.String(), nullable=False)
  email= db.Column(db.String(), nullable=False, unique = True)
  password= db.Column(db.String(), nullable=False)
  city= db.Column(db.String())
  state= db.Column(db.String())
  # org_id= db.Column(db.Integer())
  active = db.Column(db.Boolean(), nullable=False, default=True)

  def __init__ (self, first_name, last_name, email, password, city, state):
    self.first_name= first_name
    self.last_name= last_name
    self.email= email
    self.password= password
    self.city = city
    self.state= state

class UsersSchema(ma.Schema):
  class Meta:
    fields = ['user_id','first_name','last_name','email','password','city','state','active']

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)