from flask import Flask, request, jsonify
import psycopg2
import json
# import 

app = Flask(__name__)

conn = psycopg2.connect("dbname='coursedb' host='localhost' user='postgres' password='Welcome1!'")
cursor = conn.cursor()

# Users table routes

@app.route('/users/add', methods=(['POST']))
def add_user():
  form = request.form
  fname = form.get('first_name')
  if fname =='':
    return jsonify("First name is required!"), 400
  lname = form.get('last_name')
  email = form.get('email')
  if email =='':
    return jsonify("Email is required!"), 400
  password = form.get('password')
  if password =='':
    return jsonify("Password is required!"), 400
  city = form.get('city')
  state = form.get('state')
  org = form.get('organization')
  if org =='':
    return jsonify("Organization is required!"), 400
  if org.isnumeric():
    org = int(org)
  else:
    return jsonify('Org. ID must be numeric'), 400
  
  cursor.execute("INSERT INTO Users (first_name, last_name, email, password, city, state, organization) VALUES(%s,%s,%s,%s,%s,%s,%s)",(fname, lname, email, password, city, state, org))
  conn.commit()
  return jsonify('User added'), 200

@app.route('/users/edit/<user_id>', methods=(['POST']))
def edit_user(user_id):
  if user_id.isnumeric():
    user_id = int(user_id)
  else:
    return jsonify('ID must be numeric'), 400
  results = cursor.execute('SELECT user_id FROM Users WHERE user_id = %s', [user_id])
  results= cursor.fetchone()
  if results == None:
    return jsonify('No user found, please try again.'), 404
  form = request.form
  fname = form.get('first_name')
  if fname =='':
    return jsonify("First name is required!"), 400
  lname = form.get('last_name')
  email = form.get('email')
  if email =='':
    return jsonify("Email is required!"), 400
  password = form.get('password')
  if password =='':
    return jsonify("Password is required!"), 400
  city = form.get('city')
  state = form.get('state')
  org = form.get('organization')
  if org =='':
    return jsonify("Organization is required!"), 400
  if org.isnumeric():
    org = int(org)
  else:
    return jsonify('Org. ID must be numeric'), 400
  
  cursor.execute("UPDATE Users SET (first_name, last_name, email, password, city, state, organization) = (%s,%s,%s,%s,%s,%s,%s) WHERE user_id = %s",(fname, lname, email, password, city, state, org, user_id))
  conn.commit()
  return jsonify('User edited'), 200


@app.route('/users/<user_id>', methods=(['GET']))
def get_user_by_name(user_id):
  if user_id.isnumeric():
    user_id = int(user_id)
  else:
    return jsonify('user_id must be numeric'), 400
  results = cursor.execute('SELECT u.user_id, u.first_name, u.last_name, u.email, u.password, u.city, u.state, o.org_id, o.name, o.active FROM Users u JOIN organizations o On users.organization = organizations. org_id WHERE user_id = %s', [user_id])
  results= cursor.fetchone()
  if results == None:
    return jsonify('No user found, please try again.'), 404
  results_dictionary = {
    'user_id' : results[0],
    'first_name' : results[1],
    'last_name' : results[2],
    'email' : results[3],
    'password' : results[4],
    'city' : results[5],
    'state' : results[6],
    'organization' : results[7]
  }
  return jsonify(results_dictionary),200

@app.route('/users/delete/<user_id>', methods=(['DELETE']))
def delete_user_by_id(user_id):
  if user_id.isnumeric():
    user_id = int(user_id)
  else:
    return jsonify('User_id must be numeric'), 400
  result = cursor.execute('SELECT name, user_id FROM Users WHERE user_id = %s', [user_id])
  result= cursor.fetchone()
  if result == None:
    return jsonify('No user found, please try again.'), 404
  cursor.execute('DELETE from Users WHERE user_id = %s', [user_id])
  conn.commit()
  return jsonify(f'User ({result[0]}, ID#{result[1]}) deleted'), 200


@app.route('/users/list', methods=(['GET']))
def get_all_users():
  results = cursor.execute('SELECT user_id, first_name, last_name, email, password, city, state, organization FROM Users')
  results = cursor.fetchall()
  list_of_users = []

  for x in results:
    list_of_users.append({
    'user_id' : x[0],
    'first_name' : x[1],
    'email' : x[2],
    'password' : x[3],
    'size' : x[4],
    'city' : x[5],
    'state' : x[6],
    'organization' : x[7]
    })
  
  
  return jsonify({'Users' : list_of_users}),200

#Org routes

@app.route('/organizations/add', methods=(['POST']))
def add_org():
  form = request.form
  name = form.get('name')
  if name =='':
    return jsonify("Name is required!"), 400
  phone = form.get('phone')
  city = form.get('city')
  state = form.get('state')
  
  cursor.execute("INSERT INTO Organizations (name, phone, city, state) VALUES(%s,%s,%s,%s)",(name, phone, city, state))
  return jsonify('Organization added'), 200

@app.route('/organizations/edit/<org_id>', methods=(['POST']))
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


@app.route('/organizations/<org_id>', methods=(['GET']))
def get_org_by_name(org_id):
  if org_id.isnumeric():
    org_id = int(org_id)
  else:
    return jsonify('Org_id must be numeric'), 400
  results = cursor.execute('SELECT org_id, name, phone, city, state, active FROM Organizations WHERE org_id = %s', [org_id])
  results= cursor.fetchone()
  if results == None:
    return jsonify('No organization found, please try again.'), 404
  results_dictionary = {
    'org_id' : results[0],
    'name' : results[1],
    'phone' : results[2],
    'city' : results[3],
    'state' : results[4],
    'active' : results[5]
  }
  return jsonify(results_dictionary),200

@app.route('/organizations/delete/<org_id>', methods=(['DELETE']))
def delete_org_by_id(org_id):
  if org_id.isnumeric():
    org_id = int(org_id)
  else:
    return jsonify('Org_id must be numeric'), 400
  result = cursor.execute('SELECT name, org_id FROM Organizations WHERE org_id = %s', [org_id])
  result= cursor.fetchone()
  if result == None:
    return jsonify('No organization found, please try again.'), 404
  cursor.execute('DELETE from Organizations WHERE org_id = %s', [org_id])
  conn.commit()
  return jsonify(f'Organization ({result[0]}, ID#{result[1]}) deleted'), 200


@app.route('/organizations/list', methods=(['GET']))
def get_all_orgs():
  results = cursor.execute('SELECT org_id, name, phone, city, state, active FROM Organizations')
  results = cursor.fetchall()
  list_of_users = []

  for x in results:
    list_of_users.append({
    'org_id' : x[0],
    'name' : x[1],
    'phone' : x[2],
    'city' : x[3],
    'state' : x[4],
    'active' : x[5]
    })
  
  
  return jsonify({'Organizations' : list_of_users}),200


def create_all():
  cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS Organizations (
      org_id SERIAL PRIMARY KEY,
      name VARCHAR NOT NULL,
      phone VARCHAR,
      city VARCHAR,
      state VARCHAR,
      active smallint DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS Users (
      user_id serial PRIMARY KEY,
      first_name VARCHAR NOT NULL,
      last_name VARCHAR,
      email VARCHAR NOT NULL,
      password VARCHAR NOT NULL,
      city VARCHAR,
      state VARCHAR,
      organization INT NOT NULL,
      active smallint DEFAULT 1,
      FOREIGN KEY (organization)
        REFERENCES Organizations (org_id)
    );
  ''')
  data =  [["1", "Octo Studios", "555.855.5585", "San Diego", "California"],["2", "Namco", "555.867.5309", "New York City", "New York"],["3", "Skynet Tech.", "555.012.3456", "Los Angeles", "California"]]
  for x in data:
    org_id = x[0]
    print(org_id)
    name = x[1]
    phone = x[2]
    city = x[3]
    state = x[4]
    check = cursor.execute((f'SELECT org_id FROM Organizations WHERE org_id = {org_id}'))
    check = cursor.fetchone()
    if check == None:
      cursor.execute("INSERT INTO Organizations (org_id, name, phone, city, state) VALUES(%s,%s,%s,%s,%s)",(org_id, name, phone, city, state))
  data = [["100","Mark","Hoppus","mark@hoppus.net", "HappyHolidays123", "San Diego", "California","1"],["101","Tom","Delonge","tom@hoppus.net","Tak30ff!","San Diego","California","1"],["102","Travis","Barker","travis@hoppus.net","h0t4th3Kards","Los Angeles","California","1"],["103","Yugi","Yami","Yugi@oh.io","Heart0ftheC4rds","Tokyo","Japan","2"]]
  for x in data:
    user_id = x[0]
    first_name = x[1]
    last_name = x[2]
    email = x[3]
    password = x[4]
    city = x[5]
    state = x[6]
    organization = x[7]
    check = cursor.execute((f'SELECT user_id FROM Users WHERE user_id = {user_id}'))
    check = cursor.fetchone()
    if check == None:
      cursor.execute("INSERT INTO Users (user_id, first_name, last_name, email, password, city, state, organization) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(user_id, first_name, last_name, email, password, city, state, organization))
  conn.commit()
  return

if __name__ == "__main__":
  create_all()
  app.run()