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
	
    ##select rows
    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
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
    ##select rows
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    pages = [i for i in range(1,len(todos)/4+1)]
    return render_template('todos.html', todos=todos,pages = pages)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    ##A todo must have a description
    if not request.form.get('description', False) :
        return redirect('/description')

    g.db.execute(
        "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
        % (session['user']['id'], request.form.get('description', ''))
    )
    g.db.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    return redirect('/todo')


@app.route('/description')
@app.route('/description/')
def description():
    return render_template('description.html')

@app.route('/todojson/<id>', methods=['GET'])
def todojson(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    _todo = {
        'id' : id,
        'description' : todo['description'],
        'user_id'     : todo['user_id']
    }
    return json.dumps(_todo)

@app.route('/completed', methods=['POST'])
@app.route('/completed/', methods=['POST'])
def completed():
    sql = '''
        UPDATE todos SET completed = {} WHERE id = {}
    '''.format(
        0 if request.form.get('completed', 'False') == 'False' else 1,
        request.form.get('id', '0')
    )
    g.db.execute(sql)
    g.db.commit()
    return 'Done!'
