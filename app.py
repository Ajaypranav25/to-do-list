from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class my_task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = my_task(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"
    
    else:
        tasks = my_task.query.order_by(my_task.created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    delete_task = db.get_or_404(my_task, id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error: {e}"

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    task = db.get_or_404(my_task, id)

    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"

    else:
        return render_template('edit.html', task=task)



@app.route('/complete/<int:id>')
def complete(id):
    task = db.get_or_404(my_task, id)

   
    task.completed = 1 if task.completed == 0 else 0
    
    try:
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error marking complete: {e}"



if __name__ == "__main__":
    app.run(debug=True)