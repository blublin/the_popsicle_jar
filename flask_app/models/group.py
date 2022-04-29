from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

DATABASE = 'popsicle_jar'
TABLE1 = 'groups'

debug = True

class User_Group:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.users = []

    # ! Many To One, skip otherwise
    @classmethod
    def get_group_with_users( cls , data:dict ) -> object:
        query = """SELECT popsicle_jar.groups.*, users.*
                FROM group_members
                JOIN popsicle_jar.groups
                ON group_members.group_id = popsicle_jar.groups.id
                JOIN users
                ON group_members.user_id = users.id
                WHERE popsicle_jar.groups.id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db( query , data )
        group = cls( results[0] )
        if debug:
            print(results[0])
            print(f"Results: {results}")
        if not results[0]['name']:
            return user
        for data in results:
            friend_data= {
                "id" : data['groups.id'],
                "name" : data['name']
            }
            user.groups.append( group.Group( data ) )
        return user