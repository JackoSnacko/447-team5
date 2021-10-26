from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentgrades.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(80), nullable=False)
    student_grade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "{} is student_id and {} is student_name and {} is student_grade".format(self.student_id, self.student_name, student_grade)

@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method=='POST':
        student_id=request.form['student_id']
        student_name=request.form['student_name']
        student_grade=request.form['student_grade']
        new_entry = Student(student_id=student_id, student_name=student_name, student_grade=student_grade)
        db.session.add(new_entry)
        db.session.commit()
    allgrades=Student.query.all()
    return render_template('home.html', grades=allgrades)

@app.route("/delete/<int:student_id>")
def delete(student_id):
    delete_entry = Student.query.filter_by(student_id=student_id).first()
    db.session.delete(delete_entry)
    db.session.commit()
    return redirect("/")

@app.route("/updateentry/<int:student_id>", methods=['GET','POST'])
def update_entry(student_id):

    if request.method == 'POST':
        updateentry = Student.query.filter_by(student_id=student_id).first()
        student_name = request.form['student_name']
        student_grade = request.form['student_grade']
        updateentry.student_id = student_id
        updateentry.student_name = student_name
        updateentry.student_grade = student_grade
        db.session.commit()
        return redirect("/")
    updateentry = Student.query.filter_by(student_id=student_id).first()
    return render_template('update.html', updateentry=updateentry)


if __name__ == "__main__":
    app.run(debug=True)
