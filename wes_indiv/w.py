from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Foo(db.Model):
    name = db.Column(db.String(256), nullable=False)
    student_id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return '<Foo %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        points = request.form['points']
        s = Foo(name=name, student_id=id, points=points)
        try:
            db.session.add(s)
            db.session.commit()
            return redirect('/')
        except:
            return "Something fucked up"
    else:
        foo = Foo.query.order_by(Foo.student_id).all()
        return render_template('index.html', samples=foo)
    
@app.route('/delete/<int:id>')
def delete(id):
    sample_to_delete = Foo.query.get_or_404(id)
    try:
        db.session.delete(sample_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Something fucked up"

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    sample = Foo.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name']
        points = request.form['points']
        sample.name = name
        sample.points = points
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Something fucked up"
    else:
        return render_template('update.html', sample=sample)
    

if __name__ == "__main__":
    app.run(debug=True)
