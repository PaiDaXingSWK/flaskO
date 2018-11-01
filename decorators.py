#encoding:utf-8
from functools import wraps
from flask import session,redirect,url_for
def login_require(func):

    @wraps(func)
    def wrapper(*args,**kwarge):
        if session.get('user_id'):
            return func(*args,**kwarge)
        else:
            return redirect(url_for('login'))
    return wrapper