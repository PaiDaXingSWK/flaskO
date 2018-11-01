#encoding:utf-8
import os


DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = '123'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'zltk'

SQLALCHEMY_DATABASE_URI ="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS=False

DEBUG=True
SECRET_KEY=os.urandom(24)