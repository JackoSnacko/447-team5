from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request
import datetime
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covid.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


class covid_data(db.Model):
    date = db.Column(db.Integer, primary_key=True)
    allegany_cases = db.Column(db.Integer)
    anne_arundel_cases = db.Column(db.Integer)
    baltimore_county_cases = db.Column(db.Integer)
    calvert_cases = db.Column(db.Integer)
    caroline_cases = db.Column(db.Integer)
    carroll_cases = db.Column(db.Integer)
    cecil_cases = db.Column(db.Integer)
    charles_cases = db.Column(db.Integer)
    dorchester_cases = db.Column(db.Integer)
    frederick_cases = db.Column(db.Integer)
    garrett_cases = db.Column(db.Integer)
    harford_cases = db.Column(db.Integer)
    howard_cases = db.Column(db.Integer)
    kent_cases = db.Column(db.Integer)
    montgomery_cases = db.Column(db.Integer)
    prince_georges_cases = db.Column(db.Integer)
    queen_annes_cases= db.Column(db.Integer)
    st_marys_cases = db.Column(db.Integer)
    somerset_cases = db.Column(db.Integer)
    talbot_cases = db.Column(db.Integer)
    washington_cases = db.Column(db.Integer)
    wicomico_cases = db.Column(db.Integer)
    worcester_cases = db.Column(db.Integer)
    baltimore_city_cases = db.Column(db.Integer)
    allegany_deaths = db.Column(db.Integer)
    anne_arundel_deaths = db.Column(db.Integer)
    baltimore_county_deaths = db.Column(db.Integer)
    calvert_deaths = db.Column(db.Integer)
    caroline_deaths = db.Column(db.Integer)
    carroll_deaths = db.Column(db.Integer)
    cecil_deaths = db.Column(db.Integer)
    charles_deaths = db.Column(db.Integer)
    dorchester_deaths = db.Column(db.Integer)
    frederick_deaths = db.Column(db.Integer)
    garrett_deaths = db.Column(db.Integer)
    harford_deaths = db.Column(db.Integer)
    howard_deaths = db.Column(db.Integer)
    kent_deaths = db.Column(db.Integer)
    montgomery_deaths = db.Column(db.Integer)
    prince_georges_deaths = db.Column(db.Integer)
    queen_annes_deaths = db.Column(db.Integer)
    st_marys_deaths = db.Column(db.Integer)
    somerset_deaths = db.Column(db.Integer)
    talbot_deaths = db.Column(db.Integer)
    washington_deaths = db.Column(db.Integer)
    wicomico_deaths = db.Column(db.Integer)
    worcester_deaths = db.Column(db.Integer)
    baltimore_city_deaths = db.Column(db.Integer)



@app.route("/", methods=['GET', 'POST'])
def main_page():

    con = pymysql.connect(host='localhost',user='root',password='piedmont',db='covid', use_unicode=True, charset='utf8')
    cur = con.cursor()
    searchDate = "N/A"

    if(request.method=='POST'):
        color = request.form.get("color")

        searchDate=request.form['searchDate'] 
        cur.execute("SELECT * FROM covid_data WHERE Date = \""+searchDate+"\";")
        data = cur.fetchall()
        if(cur.rowcount==0):
            cur.execute("SELECT * FROM covid_data")
            data = cur.fetchall()
            searchDate = "N/A"
    else:
        color = request.form.get("color")
        cur.execute("SELECT * FROM covid_data")
        data = cur.fetchall()
    
    return render_template('states.html', covid_data=data, searchDate = searchDate, color=color)

if __name__ == "__main__":
    app.run(debug=True)