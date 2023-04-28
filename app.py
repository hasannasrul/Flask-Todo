from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.today())

    def __repr__(self) -> str:
        return f'{self.task} - {self.task}'

context = app.app_context()

with context:
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def create_read():
    if request.method == 'POST':
        if(request.form['task']=="" and request.form['desc']==""):
            return "please enter task"
            
        else:
            task = request.form['task']
            desc = request.form['desc']
            todo = Todo(task=task, desc=desc)
            db.session.add(todo)
            db.session.commit() 
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update_todo(sno):
    if request.method == 'POST':
        task = request.form['task']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.task = task
        todo.desc  = desc
        db.session.add(todo)
        db.session.commit() 
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


@app.route("/delete/<int:sno>")
def delete_todo(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=7000)