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

def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()
