from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Task = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self) -> str:
        return f'{self.sno} - {self.Task}'

context = app.app_context()

with context:
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task = request.form['task']
        desc = request.form['desc']
        todo = Todo(Task=task, desc=desc)
        db.session.add(todo)
        db.session.commit() 
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)

@app.route("/update/<int:sno>")
def update_todo(sno):
    todo = Todo(Task="First Task", desc="Go to gym")
    db.session.add(todo)
    db.session.commit() 
    allTodo = todo.query.all()
    return render_template('index.html', allTodo = allTodo)

@app.route("/delete/<int:sno>")
def delete_todo(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=7000)