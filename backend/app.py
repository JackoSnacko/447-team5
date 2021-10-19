from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import datetime


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



class Students(db.Model):
    data_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    id = db.Column(db.Integer)
    points = db.Column(db.Integer)
    date = db.Column(db.DateTime, default = datetime.datetime.now)

def __init__(self, name, id, points):
    self.name = name
    self.id = id
    self.points = points


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('data_id', 'name', 'id', 'points', 'date')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


@app.route("/read", methods = ['GET'])
def get_students():
    all_students = Students.query.all()
    results = students_schema.dump(all_students)
    return jsonify(results)


@app.route("/create", methods = ['POST'])
def add_student():
    name = request.json['name']
    id = request.json['id']
    points = request.json['points']

    students = Students(name = name, id = id, points = points)
    db.session.add(students)
    db.session.commit()
    return student_schema.jsonify(students)


@app.route("/update/<data_id>/", methods = ['PUT'])
def update_student(data_id):
    student = Students.query.get(data_id)

    name = request.json['name']
    id = request.json['id']
    points = request.json['points']

    student.name = name
    student.id = id
    student.points = points

    db.session.commit()
    return student_schema.jsonify(student)
    

@app.route("/delete/<data_id>/", methods = ['DELETE'])
def delete_student(data_id):
    student = Students.query.get(data_id)
    db.session.delete(student)
    db.session.commit()
    
    return student_schema.jsonify(student)


if __name__=="__main__":
    app.run()