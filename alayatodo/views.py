from alayatodo import app
import json
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify
    )
##Import SQL Alchemy in order to create the ORM access layer
from flask_sqlalchemy import SQLAlchemy

##Set the path to the database for SQLALCHEMY
##This is recomended by SQLAlchemy in their documentation (http://flask-sqlalchemy.pocoo.org/2.3/quickstart/#a-minimal-application)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tmp/alayatodo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
##Create the database session
db = SQLAlchemy(app)

##Create the users model
class Users(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(100),unique=True)
   password = db.Column(db.String(100))

##Create the todos model
class Todos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean,default= False)

@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    ##Use SQLALCHEMY to select rows
    ##We can't flitet just by the username, or anyone can get access
    user = Users.query.filter_by(username = username,password = password).first()
    if user:
        session['user'] = {
            'username'  : username,
            'password'  : password,
            'id'        : user.id

            }
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    ##Use SQLALCHEMY to select rows
    cur = Todos.query.filter_by(id = int(id),user_id = session['user']['id']).first()
    return render_template('todo.html', todo=cur)


@app.route('/todo', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    page = int(request.args.get('page',1))
    ##Use SQLALCHEMY to select rows
    ##Get the umber fo rows to generate pagination, this is the only way without having to execute some sql code
    rows = len(Todos.query.filter_by(user_id=session['user']['id']).all())
    page_size = 4
    ##Get the total number of pages, and create an array for pagination
    pages = [i for i in range(1,rows/page_size+1+(0 if rows%page_size ==0 else 1))]

    ##Select the Todos for the requested page
    _todos = Todos.query.filter_by(user_id=session['user']['id']).offset((page-1)*page_size).limit(page_size)
    return render_template('todos.html', todos=_todos,pages = pages)


@app.route('/todo', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    ##A todo must have a description
    if not request.form.get('description') :
        return redirect('/description')
    td = Todos(
        user_id = session['user']['id'],
        description = request.form.get('description')
        )
    db.session.add(td)
    db.session.commit()
    return redirect('/todo')


##Actually it is <int:id>(<converter:param>)
@app.route('/todo/<int:id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    cur = Todos.query.filter_by(id = id,user_id=session['user']['id']).first()
    db.session.delete(cur)
    db.session.commit()
    return redirect('/todo')


@app.route('/description')
@app.route('/description/')
def description():
    return render_template('description.html')

@app.route('/todojson/<id>', methods=['GET'])
def todojson(id):
    cur = Todos.query.filter_by(id = int(id),user_id=session['user']['id']).first()
    _todo = {
        'id' : id,
        'description' : cur.description,
        'user_id'     : cur.user_id
    }
    return jsonify(_todo)

@app.route('/completed', methods=['POST'])
@app.route('/completed/', methods=['POST'])
def completed():
    cur = Todos.query.filter_by(id = int(request.form.get('id', '0')),user_id=session['user']['id']).first()
    cur.completed = request.form.get('completed', 'False') == 'True'
    db.session.commit()
    return 'Done!'
