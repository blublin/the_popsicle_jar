from flask_bcrypt import Bcrypt
from flask import Flask, flash, session
import re

app = Flask(__name__)

app.secret_key = "XUj_GYki@2_Hw2bV6mMu" # INSERT GENERATED KEY FROM SITE