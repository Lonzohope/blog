from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(250),index=True)
    email=db.Column(db.String(250),unique=True,index=True)
    pass_secure=db.Column(db.String(255))
    about=db.Column(db.String(500))
    profile=db.Column(db.String(250))
    comments=db.relationship('Comments',backref='user',lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")
    @password.setter
    def password(self,password):
        self.pass_secure=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)



    def __repr__(self):
        return f'User {self.username}'

'''
Pitch ideas table
'''

class Blogs(db.Model):
    __tablename__="pitches"
    id=db.Column(db.Integer,primary_key=True)
    pitch=db.Column(db.String(500))
    title=db.Column(db.String(250))
    author=db.Column(db.String(250))
    categ=db.Column(db.String(250))
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return f'User {self.pitch}'

'''
Comments model
'''
#establishing a database connection
class Comments(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    pitch_id=db.Column(db.Integer)
    pitch_title=db.Column(db.String)
    comments=db.Column(db.String)
    posted=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments=Comments.query.filter_by(blog_id=id).all()
        return comments




class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(250))
    pitches=db.relationship('Pitches',backref='category',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'
