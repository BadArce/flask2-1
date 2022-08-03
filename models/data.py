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