from os import stat, path
from os.path import exists
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import pymysql
import requests


app = Flask(__name__)

def downloadFile(fileUrl,filePath):
    url = fileUrl
    req = requests.get(url)
    url_content = req.content
    csv_file = open(filePath,'wb')
    content = url_content.replace(b'"',b'')
    csv_file.write(content)
    csv_file.close()

#Constants
DB_NAME = 'covid'
TABLE_NAME = 'covid_data'
CASES_DATA_FILE_PATH = 'static/covid_confirmed_usafacts.csv'
DEATHS_DATA_FILE_PATH = 'static/covid_deaths_usafacts.csv'
POP_DATA_FILE_PATH = 'static/uscounties.csv'
VACCINATION_DATA_FILE_PATH = 'static/COVID-19_Vaccinations_in_the_United_States_County.csv'

CASES_URL = 'https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv?_ga=2.206624086.437213270.1639370301-537660709.1639370301'
DEATHS_URL = 'https://static.usafacts.org/public/data/covid-19/covid_deaths_usafacts.csv?_ga=2.250115779.437213270.1639370301-537660709.1639370301'
POP_URL = 'https://static.usafacts.org/public/data/covid-19/covid_county_population_usafacts.csv?_ga=2.186169964.437213270.1639370301-537660709.1639370301'
VACC_URL = 'https://data.cdc.gov/api/views/8xkx-amqh/rows.csv?accessType=DOWNLOAD'


#MySQL Connection
sql_connection = pymysql.connect(host='localhost',user='root',password='piedmont',db=DB_NAME, use_unicode=True, charset='utf8')


#Download Data Files
if not exists(CASES_DATA_FILE_PATH):
    downloadFile(CASES_URL,CASES_DATA_FILE_PATH)
if not exists(DEATHS_DATA_FILE_PATH):
    downloadFile(DEATHS_URL,DEATHS_DATA_FILE_PATH)
if not exists(POP_DATA_FILE_PATH):
    downloadFile(POP_URL,POP_DATA_FILE_PATH)
if not exists(VACCINATION_DATA_FILE_PATH):
    downloadFile(VACC_URL,VACCINATION_DATA_FILE_PATH)

#OPENING FILE
cases_dataFile = open(CASES_DATA_FILE_PATH,'r')
deaths_dataFile = open(DEATHS_DATA_FILE_PATH,'r')
pop_dataFile = open(POP_DATA_FILE_PATH,'r')
vacc_dataFile = open(VACCINATION_DATA_FILE_PATH,'r')

################# Cases / Deaths Formatting BEGIN

#Get column labels from cases csv file
cases_column_labels = cases_dataFile.readline().rstrip('\n').split(",")

#Gets number of rows in cases file to see if we need to update sql table
for row in cases_dataFile:
    temp = row
    for i in range(0, 4):
        c = ','
        index = temp.find(c)
        temp = temp[index + 1: ]
    new_data_cases = temp.count(',') + 1
    break

cases_dataFile.close()
cases_dataFile = open(CASES_DATA_FILE_PATH,'r')

#Database Column Names
#For loop creating sql query to create table for data

covid_column_labels = ["Date", "CountyName", "CountyFips", "State", "StateFips", "Cases", "Deaths"]

sql_data_columns = []
sql_columns = f''
for column in covid_column_labels:
    tmp_str = f''
    sql_data_columns.append(f'`'+column+f'`')
    if column == "Date":
        tmp_str = f'`{column}` DATE, '
    elif column == "CountyName":
        tmp_str = f'`{column}` VARCHAR(50), '
    elif column == "CountyFips":
        tmp_str = f'`{column}` INT, '
    elif column == "State":
        tmp_str = f'`{column}` VARCHAR(2), '
    elif column == "StateFips":
        tmp_str = f'`{column}` INT, '
    elif column == "Cases":
        tmp_str = f'`{column}` INT, '
    elif column == "Deaths":
        tmp_str = f'`{column}` INT'
    sql_columns += tmp_str
sql_columns += f', PRIMARY KEY (Date, CountyFips)'

#Execute MySQL query
cur = sql_connection.cursor()
sql = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}({sql_columns});'
try:
    cur = sql_connection.cursor()
    cur.execute(sql)
    sql_connection.commit()
except Exception as e:
    print(e)

sql_covid_columns = f'`{"Date"}`, `{"CountyName"}`, `{"CountyFips"}`, `{"State"}`, `{"StateFips"}`, `{"Cases"}`, `{"Deaths"}`'

county_fips_column = 0
county_name_column = 1
state_name_column = 2
state_fips_column = 3

sql = f'SELECT count(distinct Date) FROM covid_data;'
try:

    cur.execute(sql)
    #Checks for data in table
    old_num_dates = cur.fetchall()[0][0]
    
    #If table is not up to date
    if new_data_cases > old_num_dates:
        cur = sql_connection.cursor()
        cur.execute(f'DELETE FROM {TABLE_NAME};')

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

            if cases_line[state_name_column] == "\"MD\"":
                for i in range(4, len(cases_column_labels)):
                    if (cases_line[county_name_column][1:len(cases_line[county_name_column])-2] != "Statewide Unallocate"):
                        num_cases = 0
                        num_deaths = 0
                        sql_values = f''
                        #Date
                        sql_values += f'\'{cases_column_labels[i]}\', '
                        #County
                        sql_values += f'"{cases_line[county_name_column][1:len(cases_line[county_name_column])-2]}", '
                        #county fips
                        sql_values += f'{cases_line[county_fips_column]}, '
                        #state name
                        sql_values += f'{cases_line[state_name_column]}, '
                        #state fips
                        sql_values += f'{cases_line[state_fips_column]}, '
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
                        sql_values += f'{str(num_deaths)}'
                        
                        sql = f'INSERT INTO {TABLE_NAME}({sql_covid_columns}) VALUES({sql_values})'
                        try:
                            cur = sql_connection.cursor()
                            cur.execute(sql)
                            sql_connection.commit()
                        except Exception as e:
                            print(e)
except Exception as e:
    print(e)

################# Cases / Deaths Formatting END




################# Population Formatting BEGIN
new_data_pop = 0

for row in pop_dataFile:
    new_data_pop += 1

pop_dataFile.close()
pop_dataFile = open(POP_DATA_FILE_PATH,'r')

old_data_pop = 0
sql = f'SELECT count(countyFIPS) FROM Population;'
try:
    cur = sql_connection.cursor()
    cur.execute(sql)
    #Checks for data in table
    old_data_pop = cur.fetchall()[0][0]
except Exception as e:
    print(e)

sql_pop_columns = f'`{"CountyName"}`, `{"CountyFips"}`, `{"State"}`, `{"Population"}`'

population_column_labels = ["CountyName", "CountyFips", "State", "Population"]
sql_data_columns = []
sql_columns = f''
for column in population_column_labels:
    tmp_str = f''
    sql_data_columns.append(f'`'+column+f'`')
    if column == "CountyName":
        tmp_str = f'`{column}` VARCHAR(50), '
    elif column == "CountyFips":
        tmp_str = f'`{column}` INT, '
    elif column == "State":
        tmp_str = f'`{column}` VARCHAR(2), '
    elif column == "Population":
        tmp_str = f'`{column}` INT'
    sql_columns += tmp_str
sql_columns += f', PRIMARY KEY (CountyFips)'

if old_data_pop < new_data_pop:
    #Execute MySQL query
    cur = sql_connection.cursor()
    cur.execute(f'DROP TABLE IF EXISTS Population;')
    sql = f'CREATE TABLE IF NOT EXISTS Population ({sql_columns});'
    try:
        cur = sql_connection.cursor()
        cur.execute(sql)
        sql_connection.commit()
    except Exception as e:
        print(e)

    while True:

        #Get next line in csv file

        pop_line = pop_dataFile.readline().rstrip('\n')
        #If end of file exit
        if not pop_line:
            break
        pop_line = pop_line.split(",")
        if pop_line[4] == "\"MD\"":
            sql_values = f''
            sql_values += f'{pop_line[2]}, '
            sql_values += f'{int(pop_line[3][1:len(pop_line[3])-1])}, '
            sql_values += f'{pop_line[4]}, '
            sql_values += f'{int(pop_line[8][1:len(pop_line[8])-2])}'
            sql = f'INSERT INTO Population ({sql_pop_columns}) VALUES({sql_values})'
            try:
                cur = sql_connection.cursor()
                cur.execute(sql)
                sql_connection.commit()
            except Exception as e:
                print(e)

################# Population Formatting END


################# Vaccination Formatting BEGIN

new_max_date = vacc_dataFile.readline().rstrip('\n').rsplit(',')
new_max_date = vacc_dataFile.readline().rstrip('\n').rsplit(',')[0]

vacc_dataFile.close()
vacc_dataFile = open(VACCINATION_DATA_FILE_PATH,'r')


old_max_date = "01/01/2020"

sql = f'select max(date) from vaccination;'
try:
    cur = sql_connection.cursor()
    cur.execute(sql)
    #Checks for data in table
    old_max_date = str(cur.fetchall()[0][0])
    month = old_max_date[5:7] 
    day = old_max_date[8:10]
    year = old_max_date[0:4]
    old_max_date = month + '/' + day + '/' + year
except Exception as e:
    print(e)

sql_vacc_columns = f'`{"Date"}`, `{"CountyName"}`, `{"CountyFips"}`, `{"State"}`, `{"VaccinationPercent"}`'

## Vaccination data
vacc_column_labels = ["Date", "CountyName", "CountyFips", "State", "VaccinationPercent"]

sql_data_columns = []
sql_columns = f''
for column in vacc_column_labels:
    tmp_str = f''
    sql_data_columns.append(f'`'+column+f'`')
    if column == "Date":
        tmp_str = f'`{column}` DATE, '
    elif column == "CountyName":
        tmp_str = f'`{column}` VARCHAR(50), '
    elif column == "CountyFips":
        tmp_str = f'`{column}` INT, '
    elif column == "State":
        tmp_str = f'`{column}` VARCHAR(2), '
    elif column == "VaccinationPercent":
        tmp_str = f'`{column}` DOUBLE(4, 2)'
    sql_columns += tmp_str
sql_columns += f', PRIMARY KEY (Date, CountyFips)'

if old_max_date < new_max_date:
    #Execute MySQL query
    cur = sql_connection.cursor()
    cur.execute(f'DROP TABLE IF EXISTS Vaccination;')
    sql = f'CREATE TABLE IF NOT EXISTS Vaccination ({sql_columns});'
    try:
        cur = sql_connection.cursor()
        cur.execute(sql)
        sql_connection.commit()
    except Exception as e:
        print(e)

    vacc_line = vacc_dataFile.readline().rstrip('\n').rsplit(',')

    while True: 
        #Get next line in csv file
        vacc_line = vacc_dataFile.readline().rstrip('\n').rsplit(',')
        #If end of file exit
        if not vacc_line:
            break
        if len(vacc_line) != 32:
            break
        date = vacc_line[0]
        date_test = date
        year = date[6:10]
        month = date[0:2]
        day = date[3:5]
        date = year + '-' + month + '-' + day
        countyFips = vacc_line[1]
        countyName = vacc_line[3]
        stateName = vacc_line[4]
        vaccPercent = vacc_line[15]

        if stateName == "MD":
            if countyName not in ["Unknown County", "FIPS"]:
                sql_values = f''
                #Date
                sql_values += f'\'{date}\', '
                #County
                sql_values += f'"{countyName}", '
                #county fips
                sql_values += f'{countyFips}, '
                #state name
                sql_values += f'"{stateName}", '
                #Vacc %
                sql_values += f'{vaccPercent}'

                sql = f'INSERT INTO Vaccination ({sql_vacc_columns}) VALUES({sql_values})'
                try:
                    cur = sql_connection.cursor()
                    cur.execute(sql)
                    sql_connection.commit()
                except Exception as e:
                    print(e)
################# Vaccination Formatting END


cases_dataFile.close()
deaths_dataFile.close()
pop_dataFile.close()
vacc_dataFile.close()

#Get # of counties
cur = sql_connection.cursor()
sql = f'select count(distinct CountyName) from covid_data;'
num_counties = 0
try:
    cur = sql_connection.cursor()
    cur.execute(sql)
    sql_connection.commit()
    num_counties = cur.fetchall()[0][0]
except Exception as e:
    print(e)


@app.route("/", methods=['GET', 'POST'])
def main_page():

    cur = sql_connection.cursor()
    cur.execute("select max(distinct Date) from covid_data;")
    max_date = cur.fetchall()
    max_date = str(max_date[0][0])

    cur = sql_connection.cursor()
    cur.execute("select min(distinct Date) from covid_data;")
    min_date = cur.fetchall()
    min_date = str(min_date[0][0])

    searchDate = str(max_date[0][0])


    cur = sql_connection.cursor()
    
    if(request.method=='POST'):


        DEFAULT_COLOR = 'cases'
        color = request.form.get('color',DEFAULT_COLOR)


        DEFAULT_SEARCH_DATE  = "2020-01-22"
        searchDate=request.form.get('searchDate',DEFAULT_SEARCH_DATE)        
        if searchDate == "":
            searchDate = "2020-01-22"

        cur.execute("SELECT covid_data.Date, covid_data.CountyName, covid_data.Cases, covid_data.Deaths, Population.population, Vaccination.VaccinationPercent FROM covid_data left join Population on population.CountyFips = covid_data.CountyFips left join Vaccination on Vaccination.CountyFips = covid_data.CountyFips and Vaccination.Date = covid_data.Date WHERE covid_data.Date = \""+searchDate+"\" and covid_data.CountyName != 'Statewide Unallocate' ORDER by covid_data.CountyName ASC;")
        data = cur.fetchall()
        if(cur.rowcount==0):
            cur.execute("SELECT covid_data.Date, covid_data.CountyName, covid_data.Cases, covid_data.Deaths, Population.population, Vaccination.VaccinationPercent FROM covid_data left join Population on population.CountyFips = covid_data.CountyFips left join Vaccination on Vaccination.CountyFips = covid_data.CountyFips and Vaccination.Date = covid_data.Date;")
            data = cur.fetchall()
            searchDate = "2020-01-22"
    else:
        color = request.form.get("color")
        cur.execute("SELECT covid_data.Date, covid_data.CountyName, covid_data.Cases, covid_data.Deaths, Population.population, Vaccination.VaccinationPercent FROM covid_data left join Population on population.CountyFips = covid_data.CountyFips left join Vaccination on Vaccination.CountyFips = covid_data.CountyFips and Vaccination.Date = covid_data.Date;")
        data = list(cur.fetchall())
#parse data
    counties_data = {}
    for elem in data:
        counties_data[elem[1]] = [elem[2], elem[3], elem[4], elem[5]]
    return render_template('states.html', counties_data=counties_data, searchDate = searchDate, color=color, num_counties=num_counties, min_date=min_date, max_date=max_date)

if __name__ == "__main__":
    app.run(debug=True)