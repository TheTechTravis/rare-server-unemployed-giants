import sqlite3
import json
from models import User
from datetime import datetime

def register_user(user):    
    #open a connection to the database
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        #Set values passed in from form
        db_cursor.execute("""
        INSERT INTO Users
            ( first_name, last_name, email, password, username, created_on)
        VALUES
            ( ?, ?, ?, ?, ?, ? );
        """, (user['first_name'], user['last_name'], user['email'], user['password'], user['username'], datetime.now()))

        #Set id to id of last row, set created on to now, and account type to 1 for all (for now)
        id = db_cursor.lastrowid
        account_type_id = 1

        #Add the created things to the user being created
        user['id'] = id
        user['account_type_id'] = account_type_id
        # Add valid so they can log in, necessary client side
        user['valid'] = True

        return json.dumps(user)

def login_user(user):
    #open a connection to the database
    with sqlite3.connect("./rare.db") as conn:
        
        #dictionary cursor: makes dictionaries instead of tuples when returning rows from fetch
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        ##passing in post_body and accessing the username and password on the dictionary
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            u.bio,
            u.username,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u
        WHERE u.username = ? AND u.password = ?
        """, ( user['username'], user['password'] ))

        data = db_cursor.fetchone()
        
        #Create empty dictionary
        user = {}

        #Checks if fetchone() returned a user or None
        if data != None:
            #Add on id from the found user and add True for valid to send to client
            user['id'] = data['id']
            user['valid'] = True
            #If password incorrect or user doesn't exist, passes valid = false to client
        else:
            user['valid'] = False

        return json.dumps(user)

def get_all_users():
     
     with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            u.bio,
            u.username,
            u.profile_image_url,
            u.created_on,
            u.active
            FROM Users u
        """)

        users = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row["password"], row['bio'], row["username"], row["profile_image_url"], row['active'], row["created_on"])

            users.append(user.__dict__)

        return json.dumps(users)

def get_user_by_id(id):
     with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        #Set values passed in from form
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            u.bio,
            u.username,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u
        WHERE u.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        user = User(data['id'], data['first_name'], data['last_name'], data['email'], data["password"], data['bio'], data["username"], data["profile_image_url"], data["created_on"])

        return json.dumps(user.__dict__)

def get_user_by_email(email):
     with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        #Set values passed in from form
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            u.bio,
            u.username,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u
        WHERE u.email LIKE ?
        """, ("%" + email + "%", ))

        data = db_cursor.fetchone()

        user = {}

        # If a user is found by email, send email back to client
        if data != None:
            user['email'] = data['email']
        # If a user isn't found by email, send back empty string as email 
        else:
            user['email'] = ''

        

        return json.dumps(user)


