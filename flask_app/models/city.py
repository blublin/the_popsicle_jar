from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

DATABASE = 'popsicle_jar'
TABLE1 = 'cities'

debug = True

class City:
    def __init__( self , data ):
        self.id = data['id']
        self.city = data['city']
        self.state = data['state']
        self.zipcode = data['zipcode']

    @classmethod
    def get_one_by_zip(cls, data:dict) -> object or bool:
        query = f"SELECT * FROM {TABLE1} WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0]) if result else False