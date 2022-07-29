from random import random, randrange
from flask import flash, redirect
import re
from flask_app.config.mysqlconnetion import connectToMySQL
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id=data['id']
        self.gender=data['gender']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.others = []
        


    @staticmethod
    def validate(user):
        is_valid = True

        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid address')
            is_valid=False
        if len(user['password'])<3:
            flash('passcode not lengthy')
            is_valid=False
        if len(user['first_name'])<3:
            flash('first name not long enough')
            is_valid=False
        if len(user['last_name'])<3:
            flash('last name not long enough')
            is_valid=False
        if user['password']!= user['confirm']:
            flash('passwords must MATCH')
            is_valid=False
        
        return is_valid

    @classmethod
    def save(cls,data):
        query="INSERT into users(gender,first_name,last_name,email,password,created_at,updated_at) VALUES (%(gender)s,%(first_name)s, %(last_name)s, %(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL('practice').query_db(query,data)


    @classmethod
    def get_by_id(cls,id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("practice").query_db(query,id)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("practice").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def all_potential_matches(cls,id):
        query="SELECT * FROM users WHERE users.id != %(id)s AND users.id NOT IN( select users_id FROM matches WHERE users_id2=%(id)s union All select users_id2 FROM matches WHERE users_id=%(id)s) AND users.id NOT IN( select users_id FROM disliked WHERE users_id2=%(id)s union All select users_id2 FROM disliked WHERE users_id=%(id)s );"
        results= connectToMySQL('practice').query_db(query,id)
        potentials = []
        for user in results:
            one_user = cls(user)
            print('Hello -----------', one_user)
            potentials.append(one_user)
        print(potentials)
        if len(potentials)<1:
            return False
        return potentials[0]
        

    

    @classmethod
    def all_matches(cls,id):
        query="SELECT * FROM users WHERE users.id != %(id)s AND users.id IN( select users_id FROM matches WHERE users_id2=%(id)s union All select users_id2 FROM matches WHERE users_id=%(id)s);"
        results= connectToMySQL('practice').query_db(query,id)
        matches = []
        for user in results:
            one_user = cls(user)
            # user_data= {
            #     'id':user['users.id'],
            #     'first_name':user['first_name'],
            #     'last_name': user['last_name'],
            #     'email': user['email'],
            #     'password':user['password'],
            #     'created_at': user['users.created_at'],
            #     'updated_at': user['users.updated_at']
            # }
            matches.append(one_user)
        return matches


    @classmethod
    def move_to_match(cls,data):
        query="INSERT INTO matches(users_id,users_id2) VALUES(%(id)s,%(potentials)s)"
        return connectToMySQL('practice').query_db(query,data)

    @classmethod
    def disliked(cls,data):
        query="INSERT INTO disliked(users_id,users_id2) VALUES(%(id)s,%(potentials)s)"
        return connectToMySQL('practice').query_db(query,data)

    @classmethod
    def get_by_potential(cls,potential):
        query = "SELECT * FROM users WHERE id = %(potential)s;"
        result = connectToMySQL("practice").query_db(query,potential)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_messages_by_data(cls,data):
        query="SELECT * FROM messages Where users_id=%(id)s and users_id2 =%(potentials)s ORDER BY created_at"
        result = connectToMySQL("practice").query_db(query,data)
        messages=[]
        for message in result:
            one_message=(message)
            messages.append(one_message)
        return messages

    @classmethod
    def create_message(cls,data):
        query="INSERT INTO messages(users_id,users_id2,message,created_at) VALUES(%(id)s,%(receiver)s,%(message)s,NOW()) ON DUPLICATE KEY UPDATE message=%(message)s,created_at=NOW();"
        return connectToMySQL("practice").query_db(query,data)

    @classmethod
    def get_messages_by_data_receiver(cls,data):
        query="SELECT * FROM messages Where users_id=%(potentials)s and users_id2 =%(id)s ORDER BY created_at"
        result = connectToMySQL("practice").query_db(query,data)
        messages=[]
        for message in result:
            one_message=(message)
            messages.append(one_message)
        return messages