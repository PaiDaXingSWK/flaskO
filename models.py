#encoding:utf-8
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    tel=db.Column(db.String(11),nullable=False,unique=True)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(100),nullable=False)

    def __init__(self,*args,**kwargs):
        tel=kwargs.get('tel')
        username=kwargs.get('username')
        password=kwargs.get('password')

        self.tel=tel
        self.username=username
        self.password=generate_password_hash(password)

    def check_password(self,raw_password):
        result=check_password_hash(self.password,raw_password)
        return result
class Question(db.Model):
    __tablename__='question'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    #now（）是取服务器第一次运行的时间  now是没次创建模型当前的时间
    ccreate_timr=db.Column(db.DateTime,default=datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    author=db.relationship('User',backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__='answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time=db.Column(db.DateTime,default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    question = db.relationship('Question', backref=db.backref('answers',order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))

class Book(db.Model):
    __tablename__='book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nr = db.Column(db.Text, nullable=False)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    author = db.relationship('User', backref=db.backref('books'))