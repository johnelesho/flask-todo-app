from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todosdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       title = db.Column(db.String(100), nullable=False)
       completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
   todo_list = Todo.query.all()
   return render_template('base.html', todos = todo_list)

@app.route('/add', methods=['POST'])
def addTodo():
    todo_title = request.form["title"]
    new_todo = Todo(title=todo_title)
    db.session.add(new_todo)
    db.session.commit()

    return redirect('/')

@app.route('/update/<int:id>')
def updateTodo(id):
   
    new_todo = Todo.query.filter_by(id=id).first()
    new_todo.completed = not new_todo.completed
    db.session.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__=="__main__":
   app.run(debug=True)