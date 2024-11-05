from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    username = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    timeCreated = db.Column(db.DateTime, default=datetime.now)
    posts = db.relationship('Post',backref="user",cascade="all, delete-orphan",passive_deletes=True)
    comments = db.relationship('Comment',backref="user",cascade="all, delete-orphan",passive_deletes=True)
    
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.String(10000),nullable=False)
    photoLocation = db.Column(db.String(10000), nullable=False)
    timeCreated = db.Column(db.DateTime, default=datetime.now)
    author = db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    comments = db.relationship('Comment',backref="post",cascade="all, delete-orphan",passive_deletes=True)

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.String(1000),nullable=False)
    timeCreated = db.Column(db.DateTime, default=datetime.now)
    author = db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    postId = db.Column(db.Integer,db.ForeignKey('post.id',ondelete="CASCADE"),nullable=False)