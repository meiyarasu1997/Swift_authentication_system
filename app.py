import flask
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import or_,and_

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
        engine = create_engine('sqlite:///autentication_system.db', echo=True)
        conn = engine.connect()
        meta = MetaData()

        User_details = Table(
            'User_details', meta,
            Column('First_Name', String),
            Column('Last_Name', String),
            Column('CWS_id', String, primary_key=True),
            Column('Email_id', String),
            Column('Access_Level', String),
            Column('Password', String),
        )
        first_Name = user_name
        last_Name = user_name
        cws_id = user_name
        email_id = user_name
        access_level = user_name
        password = password

        select = User_details.select().where(
            or_(User_details.c.CWS_id == user_name, User_details.c.Email_id == user_name))
        select_obj = list = conn.execute(select)
        selected_user = select_obj.fetchall()

        if (selected_user):
            msg = "You already have an account"
            return render_template('index.html', msg=msg)
        if (password==confirm_password):
            insert_credentials(first_Name,last_Name,cws_id ,email_id,access_level,password)
            msg = "Sign up successfull"
            return render_template('index.html',msg=msg)
        else:
            msg='Password mismatch'
            return render_template('signUp.html', msg=msg)

      except:
          return 'Error occuered while signing up'
    else:
          return render_template('signUp.html')


def insert_credentials(first_Name,last_Name,cws_id ,email_id,access_level,password ):
    try:
        engine = create_engine('sqlite:///autentication_system.db', echo=True)
        conn = engine.connect()
        meta = MetaData()

        User_details = Table(
            'User_details', meta,
            Column('First_Name', String),
            Column('Last_Name', String),
            Column('CWS_id', String, primary_key=True),
            Column('Email_id', String),
            Column('Access_Level', String),
            Column('Password', String),
        )

        insertdetails = User_details.insert().values(First_Name=first_Name,
                                                     Last_Name=last_Name,
                                                     CWS_id=cws_id,
                                                     Email_id=email_id,
                                                     Access_Level=access_level,
                                                     Password=password)
        result = conn.execute(insertdetails)
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
      try:
        user_name= request.form['email']
        password = request.form['psw']
        print(user_name,password)
        engine = create_engine('sqlite:///autentication_system.db', echo=True)
        conn = engine.connect()
        meta = MetaData()

        User_details = Table(
            'User_details', meta,
            Column('First_Name', String),
            Column('Last_Name', String),
            Column('CWS_id', String, primary_key=True),
            Column('Email_id', String),
            Column('Access_Level', String),
            Column('Password', String),
        )
        select = User_details.select().where(or_(User_details.c.CWS_id == user_name, User_details.c.Email_id == user_name))
        select_obj=list=conn.execute(select)
        selected_user=select_obj.fetchall()
        if (selected_user[0][5]==password):
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
   #conect_userdetails_table()
   #insert_users()

