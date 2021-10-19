In backend/app.py, line 11, change the value to the Database URI of your local sql database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:''@localhost/crud'

cd to my-app and npm install

Run ".../CMSC447_individ/myproject/Scripts/Activate.ps1" to activate the VM. myproject is the VM directory.
Using VScode, while looking at app.py, hit F5 to start debugging. Debug using Flask and input the path to the app.py, for example mine is C:\CMSC447_individ\backend\app.py.
Next, in a terminal, cd to the my-app directory. This is the React directory. Run "npm start". This should open the UI.

This project uses flask-sqlalchemy, flask_marshmallow, flask_cors, mysqlclient, and marshmallow-sqlalchemy, so these may need to be pip installed.