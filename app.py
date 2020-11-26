import flask
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/tesDemo'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jlufufnyratasp:e3ee5445da3626f94e0df13e14696139e070591b1c51921220b8323461ebbbca@ec2-34-200-106-49.compute-1.amazonaws.com:5432/dcuebo1er73g9b'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User_details(db.Model):
    __tablename__ = 'User_details'
    First_Name = db.Column(db.String(100))
    Last_Name = db.Column(db.String(100))
    CWS_id = db.Column(db.String(20), primary_key=True)
    Email_id = db.Column(db.String(50))
    Access_Level=db.Column(db.String(50))
    Password=db.Column(db.String(20))

    def __init__(self, First_Name, Last_Name, CWS_id,Email_id,Access_Level,Password):
        self.First_Name = First_Name
        self.Last_Name = Last_Name
        self.CWS_id = CWS_id
        self.Email_id = Email_id
        self.Access_Level = Access_Level
        self.Password = Password


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
        first_Name = user_name
        last_Name = user_name
        cws_id = user_name
        email_id = user_name
        access_level = user_name
        password = password
        print('password')

        Signup_list=[]
        Signup_list


        selected_user = db.session.query(User_details).filter(User_details.CWS_id == cws_id).first()
        print("selected user")

        if (selected_user):
            msg = "Please use a different username"
            return render_template('index.html', msg=msg)
        if (password==confirm_password):
            data = User_details(first_Name,last_Name,cws_id ,email_id,access_level,password)
            db.session.add(data)
            db.session.commit()
            msg = "Sign up successfull"
            return render_template('index.html',msg=msg,email=user_name)
        else:
            msg='Password mismatch'
            return render_template('signUp.html', msg=msg)

      except Exception as error:
          return error
    else:
          return render_template('signUp.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
      try:
        user_name= request.form['email']
        password = request.form['psw']
        print(user_name,password)
        selected_user = db.session.query(User_details).filter(User_details.CWS_id == user_name).first()
        if(not selected_user):
            selected_user = db.session.query(User_details).filter(User_details.Email_id == user_name).first()
        if (selected_user.Password==password):
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
   app.run(port='1234',debug='true')
   #create_credential_table()
   #insert_credentials()
   #conect_userdetails_table()


