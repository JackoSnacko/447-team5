from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import pymysql

app = Flask(__name__)

#Constants
DB_NAME = 'covid'
TABLE_NAME = 'covid_data'
DATA_FILE_PATH = './covid_data.csv'
#MySQL Connection
sql_connection = pymysql.connect(host='localhost',user='admin',password='',db=DB_NAME, use_unicode=True, charset='utf8')

#OPENING FILE
dataFile = open(DATA_FILE_PATH,'r')

#Get column labels from csv file
column_labels = dataFile.readline().rstrip('\n').split(",")

#Database Column Names
#column_labels = ["Date","Allegany_cases","Anne Arundel_cases","Baltimore_cases","Calvert_cases","Caroline_cases","Carroll_cases","Cecil_cases","Charles_cases","Dorchester_cases","Frederick_cases","Garrett_cases","Harford_cases","Howard_cases","Kent_cases","Montgomery_cases","Prince Georges_cases","Queen Annes_cases","St. Marys_cases","Somerset_cases","Talbot_cases","Washington_cases","Wicomico_cases","Worcester_cases","Baltimore City_cases","Allegany_deaths","Anne Arundel_deaths","Baltimore_deaths","Calvert_deaths","Caroline_deaths","Carroll_deaths","Cecil_deaths","Charles_deaths","Dorchester_deaths","Frederick_deaths","Garrett_deaths","Harford_deaths","Howard_deaths","Kent_deaths","Montgomery_deaths","Prince Georges_deaths","Queen Annes_deaths","St. Marys_deaths","Somerset_deaths","Talbot_deaths","Washington_deaths","Wicomico_deaths","Worcester_deaths","Baltimore City_deaths"]

#For loop creating sql query to create table for data
sql_data_columns = []
sql_columns = f''
for column in column_labels:
    tmp_str = f''
    sql_data_columns.append(f'`'+column+f'`')
    if column == "Date":
        tmp_str = f'`{column}` DATE PRIMARY KEY,'
    elif column == column_labels[len(column_labels)-1]:
        tmp_str = f'`{column}` INT'
    else:
        tmp_str = f'`{column}` INT,'
    print(tmp_str)
    sql_columns += tmp_str

#Execute MySQL query
sql = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}({sql_columns});'
try:
    cur = sql_connection.cursor()
    cur.execute(sql)
    sql_connection.commit()
except Exception as e:
    print(e)


sql = f'SELECT count(*) FROM covid_data;'
try:
    cur.execute(sql)
    #Checks for data in table
    result = cur.fetchall()[0][0]
    #If table is not populated
    if result == 0:
        #loops through data of csv file
        while True:
            #Get next line in csv file
            line = dataFile.readline().rstrip('\n')
            
            #If end of file exit
            if not line:
                break

            #Converting date to proper sql date
            line = line.split(",")
            line[0] = f'STR_TO_DATE("{line[0]}","%m/%d/%Y")'

            sql_columns = f''
            sql_values = f''
            #loop to concatenate sql column labels and values
            for i in range(len(sql_data_columns)):
                if i == len(sql_data_columns)-1:
                    sql_columns += sql_data_columns[i]
                    sql_values += line[i]
                else:
                    sql_columns += sql_data_columns[i] + f','
                    sql_values += line[i] + f','

            #sql query to insert data into table
            sql = f'INSERT INTO {TABLE_NAME}({sql_columns}) VALUES({sql_values})'
            #print(sql)
            try:
                cur = sql_connection.cursor()
                cur.execute(sql)
                sql_connection.commit()
            except Exception as e:
                print(e)
except Exception as e:
    print(e)

dataFile.close()

@app.route("/", methods=['GET', 'POST'])
def main_page():

    cur = sql_connection.cursor()
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