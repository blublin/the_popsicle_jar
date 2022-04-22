from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import recipe
from flask import flash
import re

DATABASE = 'recipes_schema'
PRIMARY_TABLE = 'users'
# SECONDARY_TABLE = ''

debug = True

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls) -> list:
        query = f"SELECT * FROM {PRIMARY_TABLE};"
        results = connectToMySQL(DATABASE).query_db(query)
        user_list = []
        for user in results:
            user_list.append( cls(user) )
        return user_list

    @classmethod
    def get_one(cls, data:dict) -> object or bool:
        query = f"SELECT * FROM {PRIMARY_TABLE} WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0]) if result else False

    ## ! used in user validation
    @classmethod
    def get_by_col(cls, data:dict) -> object or bool:
        # Only the first key,value pair combo from dict will be checked
        query = f"SELECT * FROM {PRIMARY_TABLE} WHERE { list(data.keys())[0] } = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Return an instance class of User if true, else return False
        return cls(result[0]) if result else False

    # ! Many To One, skip otherwise
    @classmethod
    def get_single_with_many( cls , data:dict ) -> object:
        query = f"SELECT * FROM {PRIMARY_TABLE} LEFT JOIN {SECONDARY_TABLE} ON {SECONDARY_TABLE}.{PRIMARY_TABLE[:-1]}_id = {PRIMARY_TABLE}.id WHERE {PRIMARY_TABLE}.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )
        user = cls( results[0] )
        if debug:
            print(results[0])
            print(f"Results: {results}")
        for data in results:
            recipe_data= {
                "id" : data['recipes.id'],
                "name" : data['name'],
                "description" : data['description'],
                "instructions" : data['instructions'],
                "under_30" : data['under_30'],
                "origin_date" : data['origin_date'],
                "user_id" : data['user_id'],
                "created_at" : data['created_at'],
                "updated_at" : data['updated_at'],
            }
            ### CHANGE THIS TO INCLUDE CORRECT SECONDARY MODEL 
            user.recipes.append( recipe.Recipe( recipe_data ) )
            ### CHANGE THIS TO INCLUDE CORRECT SECONDARY MODEL 
        return user

    @classmethod
    def validate_model(cls, user:dict) -> bool:
        is_valid = True
        if len(user['first_name']) < 2 or not user['first_name'].isalpha():
            if debug:
                print(f"First name: {user['first_name']}")
                print(f"First name length: {len(user['first_name'])}")
                print(f"First name isalpha: {user['first_name'].isalpha()} ")
            flash("First name must be at least 2 characters an only letters.", "register")
            is_valid = False
        if len(user['last_name']) < 2 or not user['last_name'].isalpha():
            if debug:
                print(f"Last name: {user['last_name']}")
                print(f"Last name length: {len(user['last_name'])}")
                print(f"Last name isalpha: {user['last_name'].isalpha()} ")
            flash("Last name must be at least 2 characters an only letters.", "register")
            is_valid = False
        if not cls.valid_email_format(user):
            flash("Invalid email address.", "register")
            is_valid = False
        if cls.email_in_db(user):
            flash("Email in use already.", "register")
            is_valid = False
        if not cls.valid_password(user):
            is_valid = False
        return is_valid

    @staticmethod
    def valid_email_format( data:dict ) -> bool:
        # create regex pattern
        regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        match = re.search(regex, data['email'])
        if debug:
            print(f"Email: {data['email']}")
            print(match)
        return True if match else False

    @classmethod
    def email_in_db( cls, data: dict ) -> bool:
        users_emails = {user.email for user in cls.get_all()}
        # set comprehension, make a set (unique values) of all user emails
        # from the users in User.get_all()
        if debug:
            print(f"Users Email List: {users_emails}")
            print(f"User Email: {data['email']}")

        return True if data['email'] in users_emails else False
        # https://stackoverflow.com/a/40963434
        # https://stackoverflow.com/a/68438122

    @staticmethod
    def valid_password(user:dict) -> bool:
        if debug:
            print("Starting password validation.")
        # Checks matching passwords, length, contains upper, lower and digit
        is_valid = True
        if debug:
            print(f"password: {user['password']}")
            print(f"password confirm: {user['password-confirm']}")
        if user['password'] != user['password-confirm']:
            flash("Passwords do not match.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long.", "register")
            is_valid = False
        
        hasUpper = hasLower = hasDigit = False
        charInd = 0
        while (not (hasUpper and hasLower and hasDigit)) and (charInd < len(user['password'])):
            if debug:
                print("Inside password while loop.")
            # while TRUE and TRUE
            # not (A and B and C) == (not A) or (not B) or (not C)
            # True or True or True == True or False or False == True
            if user['password'][charInd].isupper(): hasUpper = True
            if user['password'][charInd].islower(): hasLower = True
            if user['password'][charInd].isdigit(): hasDigit = True
            charInd += 1
        if debug:
            print("End password while loop")
        if not (hasUpper and hasLower and hasDigit):
            flash("Password must contain at least 1 lower character, 1 upper character and a digit.", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def save(data):
        query = f"INSERT INTO {PRIMARY_TABLE} ( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );"
        return connectToMySQL(DATABASE).query_db( query, data )

    @staticmethod
    def del_one(data):
        query = f"DELETE FROM {PRIMARY_TABLE} WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @staticmethod
    def update(data):
        query = f"UPDATE {PRIMARY_TABLE} SET name = %(name)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db( query, data )