from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sqlite3
from sqlite3 import Error
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signUp')
def signUp():
    return render_template("signUp.html")

@app.route('/newuser', methods=['POST'])
def newuser():
    if request.method == 'POST':
      try:
        user_name= request.form['email']
        password = request.form['psw']
        confirm_password = request.form['psw-repeat']
        sqliteConnection = sqlite3.connect('SQLite.db')  # need to define some db for our use
        cursor = sqliteConnection.cursor()  # connecting to SQL lite
        select_record = """select * from credential_table where cwsid="{}" """.format(user_name)
        users_detail = cursor.execute(select_record).fetchall()
        sqliteConnection.commit()
        cursor.close()
        if (users_detail):
            msg = "You already have an account"
            return render_template('index.html', msg=msg)
        if (password==confirm_password):
            insert_credentials(user_name,password)
            msg = "Sign up successfull"
            return render_template('index.html',msg=msg)
        else:
            msg='Password mismatch'
            return render_template('signUp.html', msg=msg)

      except:
          return 'Error occuered while signing up'
    else:
          return render_template('signUp.html')


def create_credential_table():
    try:
        sqliteConnection = sqlite3.connect('SQLite.db')
        sqlite_create_table_query = '''CREATE TABLE credential_table (
                                    cwsid TEXT PRIMARY KEY,
                                    password TEXT NOT NULL);'''
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def insert_credentials(cwsid,password):
    try:
        sqliteConnection = sqlite3.connect('SQLite.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_query = """INSERT INTO credential_table
                              (cwsid, password) 
                              VALUES ('{}', '{}');""".format(cwsid,password)
        cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if (sqliteConnection):
            print("Total Rows affected since the database connection was opened: ", sqliteConnection.total_changes)
            sqliteConnection.close()
            print("sqlite connection is closed")


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
      try:
        user_name= request.form['email']
        password = request.form['psw']
        print(user_name,password)
        sqliteConnection = sqlite3.connect('SQLite.db')#need to define some db for our use
        cursor = sqliteConnection.cursor()  #connecting to SQL lite
        select_record= """select * from credential_table where cwsid="{}" and password="{}" """.format(user_name,password)
        users_detail=cursor.execute(select_record).fetchall()
        sqliteConnection.commit()
        cursor.close()
        if (users_detail):
            msg = "sucessfully logged in"
            return render_template('index.html', msg=msg)
        else:
            msg = "Incorrect username/password!"
            return render_template('index.html', msg=msg)
      except:
            return 'Error occuered while logging in'
    else:
        return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)
   #create_credential_table()
   #insert_credentials()


