from flask import Flask, g
import sqlite3
import os

# configuration
##Use python os functions to create a path for cross platform usability
##I don't think we do need to cerate a temp file here, i just used this so the code can still run in both windows and linux(due to the \ / issue)
DATABASE = os.path.join('tmp','alayatodo.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)

#This must be called after the app is created, otherwise you can't import app from views
import views

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
