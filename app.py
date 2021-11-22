from os import stat
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import pymysql

app = Flask(__name__)

#Constants
DB_NAME = 'covid'
TABLE_NAME = 'covid_data'
CASES_DATA_FILE_PATH = '/Users/jackbitzel/Desktop/447-team5-main/static/covid_confirmed_usafacts.csv'
DEATHS_DATA_FILE_PATH = '/Users/jackbitzel/Desktop/447-team5-main/static/covid_deaths_usafacts.csv'
#MySQL Connection
sql_connection = pymysql.connect(host='localhost',user='root',password='piedmont',db=DB_NAME, use_unicode=True, charset='utf8')

#OPENING FILE
cases_dataFile = open(CASES_DATA_FILE_PATH,'r')
deaths_dataFile = open(DEATHS_DATA_FILE_PATH,'r')

#Get column labels from csv file
cases_column_labels = cases_dataFile.readline().rstrip('\n').split(",")


#Database Column Names
#column_labels = ["Date","Allegany_cases","Anne Arundel_cases","Baltimore_cases","Calvert_cases","Caroline_cases","Carroll_cases","Cecil_cases","Charles_cases","Dorchester_cases","Frederick_cases","Garrett_cases","Harford_cases","Howard_cases","Kent_cases","Montgomery_cases","Prince Georges_cases","Queen Annes_cases","St. Marys_cases","Somerset_cases","Talbot_cases","Washington_cases","Wicomico_cases","Worcester_cases","Baltimore City_cases","Allegany_deaths","Anne Arundel_deaths","Baltimore_deaths","Calvert_deaths","Caroline_deaths","Carroll_deaths","Cecil_deaths","Charles_deaths","Dorchester_deaths","Frederick_deaths","Garrett_deaths","Harford_deaths","Howard_deaths","Kent_deaths","Montgomery_deaths","Prince Georges_deaths","Queen Annes_deaths","St. Marys_deaths","Somerset_deaths","Talbot_deaths","Washington_deaths","Wicomico_deaths","Worcester_deaths","Baltimore City_deaths"]

#For loop creating sql query to create table for data

column_labels = ["Date", "County", "Cases", "Deaths"]
sql_data_columns = []
sql_columns = f''

for column in column_labels:
    tmp_str = f''
    sql_data_columns.append(f'`'+column+f'`')
    if column == "Date":
        tmp_str = f'`{column}` DATE, '
    elif column == "County":
        tmp_str = f'`{column}` VARCHAR(25), '
    elif column == column_labels[len(column_labels)-1]:
        tmp_str = f'`{column}` INT'
    else:
        tmp_str = f'`{column}` INT,'
    sql_columns += tmp_str

sql_columns += f', PRIMARY KEY (Date, County)'

#Execute MySQL query
cur = sql_connection.cursor()
cur.execute(f'DROP TABLE IF EXISTS {TABLE_NAME};')
sql = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}({sql_columns});'
try:
    cur = sql_connection.cursor()
    cur.execute(sql)
    sql_connection.commit()
except Exception as e:
    print(e)

sql_columns = f'`{"Date"}`, `{"County"}`, `{"Cases"}`, `{"Deaths"}`'

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
            cases_line = cases_dataFile.readline().rstrip('\n')
            deaths_line = deaths_dataFile.readline().rstrip('\n')

            #If end of file exit
            if not cases_line:
                break
            
            cases_line = cases_line.split(",")
            deaths_line = deaths_line.split(",")

            sql = f''

            if cases_line[2] == "\"MD\"":
                for i in range(4, len(cases_column_labels)):
                    num_cases = 0
                    num_deaths = 0
                    sql_values = f''
                    #Date
                    sql_values += f'\'{cases_column_labels[i]}\', '
                    #County
                    sql_values += f'"{cases_line[1][1:len(cases_line[1])-2]}", '
                    #Cases
                    if i > 4:
                        num_cases = int(cases_line[i]) - int(cases_line[i-1])
                    else:
                        num_cases = int(cases_line[i])
                    if num_cases < 0:
                        num_cases = 0
                    sql_values += f'{str(num_cases)}, '
                    #Deaths
                    if i > 4:
                        num_deaths = int(deaths_line[i]) - int(deaths_line[i-1])
                    else:
                        num_deaths = int(deaths_line[i])
                    if num_deaths < 0:
                        num_deaths = 0
                    sql_values += str(num_deaths)
                    
                    sql = f'INSERT INTO {TABLE_NAME}({sql_columns}) VALUES({sql_values})'
                    try:
                        cur = sql_connection.cursor()
                        cur.execute(sql)
                        sql_connection.commit()
                    except Exception as e:
                        print(e)
except Exception as e:
    print(e)

cases_dataFile.close()
deaths_dataFile.close()

@app.route("/", methods=['GET', 'POST'])
def main_page():

    cur = sql_connection.cursor()
    searchDate = "N/A"

    if(request.method=='POST'):
        color = request.form.get("color")

        searchDate=request.form['searchDate'] 
        cur.execute("SELECT * FROM covid_data WHERE Date = \""+searchDate+"\" and County != 'Statewide Unallocate' ORDER by County ASC;")
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