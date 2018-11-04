# encoding:utf-8
from flask import Flask,render_template,request,redirect,url_for,session
import config
from sqlalchemy import or_
from models import User,Question
from exts import db
from decorators import login_require
from functools import wraps
app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)
#登陆限制装饰器
# def login_require(func):
#
#     @wraps(func)
#     def wrapper(*args,**kwarge):
#         if session.get('user_id'):
#             return func(*args,**kwarge)
#         else:
#             return redirect(url_for('login'))
#     return wrapper

@app.route('/')
def index():
    context={
        'questions':Question.query.order_by('-ccreate_timr').all()
    }
    return render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        tel = request.form.get('tel')
        password = request.form.get('password')
        user=User.query.filter(User.tel==tel).first()
        if user and user.check_password(password):
            session['user_id']=user.id
            #31天内不需要再登陆
            session.permanent=True
            #return render_template('index.html')
            return redirect(url_for('index'))
        else:
            return 'error'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method=='GET':
        return render_template('regist.html')
    else:
        tel=request.form.get('tel')
        username=request.form.get('username')
        password=request.form.get('password')
        #校验已经注册就无法注册
        user=User.query.filter(User.tel==tel).first()
        if user:
            return u'此手机已被注册'
        else:
            user=User(tel=tel,username=username,password=password)
            db.session.add(user)
            db.session.commit()

            #跳转登陆页面
            return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))

@app.route('/search/')
def search():
    q=request.args.get('q')
    questions=Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-ccreate_timr')
    return render_template('index.html',questions=questions)

@app.route('/question/',methods=['GET','POST'])
@login_require
def question():
    if request.method=='GET':
        return render_template('question.html')
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        question=Question(title=title,content=content)
        user_id=session.get('user_id')
        user=User.query.filter(User.id==user_id).first()
        question.author=user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))
@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()

    return render_template('detail.html',question=question_model)

@app.route('/add_answer/',methods=['POST'])
def add_answer():
    request.form.get('answer_content')



@app.context_processor
def my_context_processor():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            return {'user':user}
    return {}
if __name__ == '__main__':
    app.run()
