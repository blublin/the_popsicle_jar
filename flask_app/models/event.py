from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import recipe
from flask import flash
from datetime import datetime
import re

DATABASE = 'popsicle_jar'
TABLE1 = 'events'
TABLE2 = 'users'

debug = True

class Event:
    def __init__(self, data:dict) -> None:
        ## INSTANCE ATTRIBUTES SHOULD BE SAME AS TABLE COLUMNS
        self.id = data['id']
        self.name = data['name']
        self.when = Event.convertWhen(data['when']) # WRITE THIS METHOD
        self.location = Event.getLocation(data['city_id']) # WRITE THIS METHOD
        self.twentyOnePlus = data['twentyOnePlus']
        self.description = data['description']
        self.activity_type = Event.getType(data['activity_id']) # WRITE THIS METHOD
        self.creator_id = data['creator_id'] # ROUTE NEEDS TO CONVERT TO NAME
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.many = [] # if many to one, store many here ## Ex: Dojo and Ninjas