from flask import render_template,redirect,url_for,flash,request
from . import auth
from .forms import RegisterForm,LoginForm
from .. import db
from ..models import Users
from flask_login import login_user,logout_user,login_required


@auth.route("/login",methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Invalid Username or Password")
    title="Blog Login"
    return render_template("auth/login.html",title=title,login=form)

@auth.route("/register",methods=['POST',"GET"])
def register():
    title="Registration"
    form=RegisterForm()
    if form.validate_on_submit():
        user=Users(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for(".login"))


    return render_template("auth/register.html",registration=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
