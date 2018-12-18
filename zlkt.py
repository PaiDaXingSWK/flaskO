# encoding:utf-8
from flask import Flask,render_template,request,redirect,url_for,session,flash
import config
from sqlalchemy import or_
from models import User,Question,Answer,Book
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

@app.route('/index/')
def index():
    page = int(request.args.get('page', 1))  # 当前页数
    per_page = int(request.args.get('per_page', 5))  # 设置每页数量
    paginate =Question.query.order_by('-ccreate_timr').paginate(page, per_page, error_out=False)
    questions=paginate.items
    # context = {
    #     'questions': Question.query.order_by('-ccreate_timr').all()
    # }
    # return render_template('index.html', **context)
    return render_template('index.html',paginate=paginate,questions=questions)

@app.route('/search/')
def search():
    q=request.args.get('q')
    page = int(request.args.get('page', 1))  # 当前页数
    per_page = int(request.args.get('per_page', 5))  # 设置每页数量
    paginate =Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-ccreate_timr').paginate(page,per_page,False)
    questions=paginate.items
    return render_template('search.html',questions=questions,paginate=paginate,q=q)

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
            #flash("标签名称已经存在! ", "error")

            flash(u'账号或密码密码错误，请重新输入','error')
           # return 'Invalid credentials'
            return redirect(url_for('login'))



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
    page = int(request.args.get('page', 1))  # 当前页数
    per_page = int(request.args.get('per_page', 5))  # 设置每页数量
    question_model=Question.query.filter(Question.id==question_id).first()
    count=Answer.query.filter(Answer.question_id==question_id).count()
    paginate=Answer.query.filter(Answer.question_id==question_id).order_by(Answer.create_time.desc()).paginate(page, per_page, error_out=False)
    aa=paginate.items
    return render_template('detail.html',paginate=paginate,question=question_model,count=count,aa=aa,q=question_id)

@app.route('/add_answer/',methods=['POST'])
@login_require
def add_answer():
    content=request.form.get('answer_content')
    question_id=request.form.get('question_id')

    answer=Answer(content=content)
    user_id=session['user_id']
    user=User.query.filter(User.id==user_id).first()
    answer.author=user
    question=Question.query.filter(Question.id==question_id).first()
    answer.question=question
    db.session.add(answer)
    db.session.commit()

    return redirect(url_for('detail',question_id=question_id))

@app.route('/del_book/<del_id>/')
def del_book(del_id):
        print del_id
        book = Book.query.filter(Book.id == del_id).first()
        db.session.delete(book)
        db.session.commit()
        return render_template('book.html')

@app.route('/add_book/',methods=['GET','POST'])
@login_require
def add_book():
    if request.method=='GET':
        return render_template('book.html')
    else:
        nr = request.form.get('nr')
        book=Book(nr=nr)
        author_id = session['user_id']
        authord = User.query.filter(User.id == author_id).first()
        book.author=authord
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('add_book',author_id=author_id))

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



