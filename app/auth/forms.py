from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField
from wtforms.validators import Required,Email,EqualTo
from .. models import Users


class RegisterForm(FlaskForm):
    email=StringField("Enter your Email",validators=[Required(),Email(),EqualTo('mail_confirm',message="Emails dont match")])
    mail_confirm=StringField("Confirm Email",validators=[Required(),Email()])
    username=StringField("Enter your Username",validators= [Required()])
    password=PasswordField("Password",validators=[Required(),EqualTo('password_confirm',message="Password must Match")])
    password_confirm=PasswordField("Confirm password",validators=[Required()])
    submit=SubmitField("Sign Up")
    def validate_email(self,data_field):
        if Users.query.filter_by(email =data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if Users.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')


class LoginForm(FlaskForm):
    email=StringField("Your email Address",validators=[Required(),Email()])
    password=PasswordField("Password",validators=[Required()])
    remember=BooleanField("Remember Me")
    submit=SubmitField("Sign In")
