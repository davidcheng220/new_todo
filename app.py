from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#init flask app
app = Flask(__name__)

# set config dictionary
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create a database table
class Todo(db.Model):
    todo_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    
# flask server routes
@app.route('/')
def home():
    #show all todos
    todo_list = Todo.query.all()
    # print todo list
    # print(todo_list)
    return render_template('index.html', todo_list=todo_list)

@app.route("/add", methods = ["POST"])
def add():
    #add new item
    title = request.form.get("title")
    new_todo = Todo(title = title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    #update the task and show complete
    todo = Todo.query.filter_by(todo_id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # delete the task
    todo = Todo.query.filter_by(todo_id=todo_id).first() #important!!! first var is for the db col and the second is for app id 
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return "about"
# run server
if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
        # try to add so item in todo database
        # new_todo = Todo(title = "todo 1", complete = False)
        # db.session.add(new_todo)
        # db.session.commit()
        
        app.run(debug = True) #ddebug mode on