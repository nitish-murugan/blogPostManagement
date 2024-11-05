from flask import Blueprint,render_template,redirect,url_for,request
from . import db
from .model import User
from flask import flash
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash

auth = Blueprint("auth",__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        emailAdr = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=emailAdr).first()
        if user:
            if check_password_hash(user.password,password):
                flash("User login success",category="success")
                login_user(user,remember=True)
                return redirect(url_for("view.home"))
            else:
                flash("Invalid password",category="error")
        else:
            flash("Email address doesn't exists",category="error")
    return render_template("login.html",user=current_user)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        emailAdr = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        rpassword = request.form.get("rpassword")
        
        emailExists = User.query.filter_by(email=emailAdr).first()
        usernameExists = User.query.filter_by(username=username).first()
        
        if(emailExists):
            flash("Email address already exists! ",category='error')
        elif(usernameExists):
            flash("Username already exists! ",category='error')
        elif(password != rpassword):
            flash("Password doesn't match! ",category='error')
        else:
            newUser = User(email=emailAdr,username=username,password=generate_password_hash(password,method="pbkdf2:sha256"))
            db.session.add(newUser)
            db.session.commit()
            flash("User created ")
            login_user(newUser,remember=True)
            return redirect(url_for("view.home"))
    return render_template("signup.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("view.home"))
