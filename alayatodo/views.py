from alayatodo import app
import json
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
    )
##Import the models from __init__
from __init__ import users,db
from __init__ import todos as _todos

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
    user = users.query.filter_by(username = username).filter_by(password = password).first()
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
    cur = _todos.query.filter_by(id = int(id)).first()
    return render_template('todo.html', todo=cur)


@app.route('/todo', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    page = int(request.args.get('page',1))
    ##Use SQLALCHEMY to select rows
    todos = _todos.query.filter_by(user_id = session['user']['id']).all()
    ##Get the total number of pages, and create an array for pagination
    pages = [i for i in range(1,len(todos)/4+1+(0 if len(todos)%4 ==0 else 1))]
    ##Select the todos for the requested page
    todos = todos[(page-1)*4:page*4]
    return render_template('todos.html', todos=todos,pages = pages)


@app.route('/todo', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    ##A todo must have a description
    if not request.form.get('description', False) :
        return redirect('/description')
    td = _todos(
        user_id = session['user']['id'],
        description = request.form.get('description', '')
        )
    db.session.add(td)
    db.session.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    cur = _todos.query.filter_by(id = int(id)).first()
    db.session.delete(cur)
    db.session.commit()
    return redirect('/todo')


@app.route('/description')
@app.route('/description/')
def description():
    return render_template('description.html')

@app.route('/todojson/<id>', methods=['GET'])
def todojson(id):
    cur = _todos.query.filter_by(id = int(id)).first()
    __todo = {
        'id' : id,
        'description' : cur.description,
        'user_id'     : cur.user_id
    }
    return json.dumps(__todo)

@app.route('/completed', methods=['POST'])
@app.route('/completed/', methods=['POST'])
def completed():
    cur = _todos.query.filter_by(id = int(request.form.get('id', '0'))).first()
    cur.completed = request.form.get('completed', 'False') == 'True'

    db.session.commit()
    return 'Done!'
