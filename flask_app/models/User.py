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