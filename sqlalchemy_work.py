from uuid import UUID
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import json
from flask_marshmallow import Marshmallow
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid
from datetime import datetime

app = Flask(__name__)
database_host = "ec2-44-206-137-96.compute-1.amazonaws.com"
database_name = "d5enhbvgtojj6e"
database_username = "vwskpgcmqizdpc"
database_password = "852e0d06674f0442b34464967bff60b1194b0d93150af5c78410eee62a7fb2e9"
app.config['SQLALCHEMY_DATABASE_URI'] = F'postgresql://{database_username}:{database_password}@{database_host}:5432/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
conn = psycopg2.connect(f"dbname='{database_name}' host='{database_host}' user='{database_username}' password='{database_password}'")
cursor = conn.cursor()
db = SQLAlchemy(app)
ma = Marshmallow(app)


class AppOrgs(db.Model):
  __tablename__ = "organizations"
  org_id = db.Column(db.Integer(), primary_key=True)
  name= db.Column(db.String(), nullable=False)
  phone= db.Column(db.String())
  city= db.Column(db.String())
  state= db.Column(db.String())
  active = db.Column(db.Boolean(), nullable=False, default=True)

  def __init__ (self, name, phone, city, state):
    self.name= name
    self.phone= phone
    self.city = city
    self.state= state
    self.active = True

class OrgsSchema(ma.Schema):
  class Meta:
    fields = ['org_id','name','phone','city','state','active']

org_schema = OrgsSchema()
orgs_schema = OrgsSchema(many=True)

class AppUsers(db.Model):
  __tablename__ = "users"
  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  first_name= db.Column(db.String(), nullable=False)
  last_name= db.Column(db.String(), nullable=False)
  email= db.Column(db.String(), nullable=False, unique = True)
  password= db.Column(db.String(), nullable=False)
  city= db.Column(db.String())
  state= db.Column(db.String())
  org_id= db.Column(db.Integer(), db.ForeignKey(AppOrgs.org_id))
  role = db.Column(db.String(), nullable=False, default='user')
  active = db.Column(db.Boolean(), nullable=False, default=True)

  def __init__ (self, first_name, last_name, email, password, city, state,org_id, role):
    self.first_name= first_name
    self.last_name= last_name
    self.email= email
    self.password= password
    self.city = city
    self.state= state
    self.org_id = org_id
    self.role = role
    self.active = True

class UsersSchema(ma.Schema):
  class Meta:
    fields = ['user_id','first_name','last_name','email','city','state','org_id','role','active']

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


def create_all():
  db.create_all()
  print("Querying for Super Admin user . . .")
  user_data = db.session.query(AppUsers).filter(AppUsers.email == 'admin@devpipeline.com').first()
  if user_data == None:
    password = 1234
    # print('App User not Found, creating Super Admin (admin@devpipeline.com). . . ')
    # password = ''
    # while password == "":
    #   password = input('Please enter a new SuperAdmin password: ')

    org_record = AppOrgs('Dev Pipeline','','Orem','UT')
    record = AppUsers('Super', 'Admin', 'admin@devpipeline.com', password, 'Orem', 'UT', 1, 'super-admin')
    db.session.add(org_record)
    db.session.commit()
    db.session.add(record)
    db.session.commit()

# def populate_dbs():

#   data =  [["1", "Octo Studios", "555.855.5585", "San Diego", "California"],["2", "Namco", "555.867.5309", "New York City", "New York"],["3", "Skynet Tech.", "555.012.3456", "Los Angeles", "California"]]
#   for x in data:
#     org_id = x[0]
#     print(org_id)
#     name = x[1]
#     phone = x[2]
#     city = x[3]
#     state = x[4]
#     check = cursor.execute((f'SELECT org_id FROM Organizations WHERE org_id = {org_id}'))
#     check = cursor.fetchone()
#     if check == None:
#       cursor.execute("INSERT INTO Organizations (org_id, name, phone, city, state) VALUES(%s,%s,%s,%s,%s)",(org_id, name, phone, city, state))
#   data = [["100","Mark","Hoppus","mark@hoppus.net", "HappyHolidays123", "San Diego", "California","1"],["101","Tom","Delonge","tom@hoppus.net","Tak30ff!","San Diego","California","1"],["102","Travis","Barker","travis@hoppus.net","h0t4th3Kards","Los Angeles","California","1"],["103","Yugi","Yami","Yugi@oh.io","Heart0ftheC4rds","Tokyo","Japan","2"]]
#   for x in data:
#     user_id = x[0]
#     first_name = x[1]
#     last_name = x[2]
#     email = x[3]
#     password = x[4]
#     city = x[5]
#     state = x[6]
#     org_id = x[7]
#     check = cursor.execute((f'SELECT user_id FROM Users WHERE user_id = {user_id}'))
#     check = cursor.fetchone()
#     if check == None:
#       cursor.execute("INSERT INTO Users (user_id, first_name, last_name, email, password, city, state, organization) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(user_id, first_name, last_name, email, password, city, state, organization))
#   conn.commit()
#   return




# if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
#   create_all()
#   db.init_app(app)


# Users table routes

@app.route('/users/add', methods=(['POST']))
def add_user():
  form = request.form
  fields = ['first_name','last_name','email','password','city','state','org_id','role']
  req_fields = ['first_name','last_name','email','password']
  values = []

  for field in fields:
    form_value = form.get(field)
    if form_value in req_fields and form_value == " ":
      return jsonify(f'{field} is a required field'), 400
    values.append(form_value)

  first_name = form.get('first_name')
  last_name = form.get('last_name')
  email = form.get('email')
  password = form.get('password')
  city = form.get('city')
  state = form.get('state')
  org_id = form.get('org_id')
  if org_id == '':
    org_id = None
  role = form.get('role')

  new_user_record = AppUsers(first_name, last_name, email, password, city, state, org_id, role)
  db.session.add(new_user_record)
  db.session.commit()
  
  return jsonify('User added'), 200


@app.route('/users/edit/<user_id>', methods=(['POST']))
def edit_user(user_id, first_name = None, last_name = None, email = None, password = None, city = None, state = None, role = None, active = None):
  user_record = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
  if user_record == None:
    return jsonify('No user found, please try again.'), 404
  if request:
    form = request.form
    first_name = form.get('first_name')
    last_name = form.get('last_name')
    email = form.get('email')
    password = form.get('password')
    city = form.get('city')
    state = form.get('state')
    role = form.get('role')
    active = form.get('active')

  if first_name:
    user_record.first_name = first_name
  if last_name:
    user_record.last_name = last_name
  if email:
    user_record.email = email
  if password:
    user_record.password = password
  if city:
    user_record.city = city
  if state:
    user_record.state = state
  if role:
    user_record.role = role
  if active:
    user_record.active = active

  db.session.commit()
  return jsonify('User edited'), 200

@app.route('/users/activate/<user_id>', methods=(['PUT']))
def activate_user(user_id):
  user_record = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
  if user_record == None:
    return jsonify('No user found, please try again.'), 404
  user_record.active = True
  db.session.commit()
  return jsonify('User activated'), 200

@app.route('/users/deactivate/<user_id>', methods=(['PUT']))
def deactivate_user(user_id):
  user_record = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
  if user_record == None:
    return jsonify('No user found, please try again.'), 404
  user_record.active = False
  db.session.commit()
  return jsonify('User deactivated'), 200



@app.route('/users/<user_id>', methods=(['GET']))
def get_user_by_id(user_id):
  user_record = db.session.query(AppUsers).filter(AppUsers.user_id==user_id).first()
  return jsonify(users_schema.dump(user_record)),200

@app.route('/users/delete/<user_id>', methods=(['DELETE']))
def delete_user_by_id(user_id):
  result = cursor.execute('SELECT first_name, user_id FROM users WHERE user_id = %s', [user_id])
  result= cursor.fetchone()
  if result == None:
    return jsonify('No user found, please try again.'), 404
  cursor.execute('DELETE fROM users WHERE user_id = %s', [user_id])
  conn.commit()
  return jsonify(f'User ({result[0]}, ID#{result[1]}) deleted'), 200


@app.route('/users/list', methods=(['GET']))
def get_all_users():
  user_records = db.session.query(AppUsers).all()
  return jsonify(users_schema.dump(user_records)),200

# #Org routes

@app.route('/orgs/add', methods=(['POST']))
def add_org():
  form = request.form
  name = form.get('name')
  if name =='':
    return jsonify("Name is required!"), 400
  phone = form.get('phone')
  city = form.get('city')
  state = form.get('state')
  active = True
  
  cursor.execute("INSERT INTO Organizations (name, phone, city, state, active) VALUES(%s,%s,%s,%s,%s);",(name, phone, city, state,active))
  return jsonify('Organization added'), 200

@app.route('/orgs/edit/<org_id>', methods=(['POST']))
def edit_org(org_id):
  if org_id.isnumeric():
    org_id = int(org_id)
  else:
    return jsonify('ID must be numeric'), 400
  results = cursor.execute('SELECT org_id FROM Organizations WHERE org_id = %s', [org_id])
  results= cursor.fetchone()
  if results == None:
    return jsonify('No organization found, please try again.'), 404
  form = request.form
  name = form.get('name')
  if name =='':
    return jsonify("Name is required!"), 400
  phone = form.get('phone')
  city = form.get('city')
  state = form.get('state')
  
  cursor.execute("UPDATE Organizations SET (name, phone, city, state) = (%s,%s,%s,%s) WHERE org_id = %s",(name, phone, city, state, org_id))
  conn.commit()
  return jsonify('Organization edited'), 200


@app.route('/orgs/<org_id>', methods=(['GET']))
def get_org_by_id(org_id):
  org_records = db.session.query(AppOrgs).filter(AppOrgs.org_id==org_id).first()
  return jsonify(users_schema.dump(org_records)),200

@app.route('/orgs/delete/<org_id>', methods=(['DELETE']))
def delete_org_by_id(org_id):
  if org_id.isnumeric():
    org_id = int(org_id)
  else:
    return jsonify('Org_id must be numeric'), 400
  result = cursor.execute('SELECT name, org_id FROM Organizations WHERE org_id = %s', [org_id])
  result= cursor.fetchone()
  if result == None:
    return jsonify('No organization found, please try again.'), 404
  else:
    cursor.execute('DELETE from Organizations WHERE org_id = %s', [org_id])
    conn.commit()
    return jsonify(f'Organization ({result[0]}, ID#{result[1]}) deleted'), 200


@app.route('/orgs/list', methods=(['GET']))
def get_all_orgs():
  org_records = db.session.query(AppOrgs).all()
  return jsonify(users_schema.dump(org_records)),200



if __name__ == "__main__":
  create_all()
  # populate_dbs()
  app.run()