from flask import Flask, g
import sqlite3
import os
##Import SQL Alchemy in order to create the ORM access layer
from flask_sqlalchemy import SQLAlchemy

# configuration
##Use python os functions to create a path for cross platform usability
DATABASE = os.path.join('tmp','alayatodo.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
##Set the path to the database for SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tmp/alayatodo.db'
##Create the database session
db = SQLAlchemy(app)

##Create the users model
class users(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(100))
   password = db.Column(db.String(100))

##Create the todos model
class todos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(100))
    completed = db.Column(db.Boolean)

##These functions are not needed, access to the db is handled by SQLAlchemy
#def connect_db():
#    conn = sqlite3.connect(app.config['DATABASE'])
#    conn.row_factory = sqlite3.Row
#    return conn


#@app.before_request
#def before_request():
#    g.db = connect_db()


#@app.teardown_request
#def teardown_request(exception):
#    db = getattr(g, 'db', None)
#    if db is not None:
#        db.close()


import alayatodo.views
