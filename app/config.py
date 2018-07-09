import os
import pymysql
# dialect+driver://username:password@host:port/database
DEBUG=True
SECRET_KEY=os.urandom(24)
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '0130'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'run_into_movies'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST
                                             ,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False 

# MAIL_SERVER = 'smtp.qq.com',
# MAIL_PORT = 465,
# MAIL_USE_TLS = False,
# MAIL_USE_SSL = True,
# MAIL_PASSWORD = '**********',#看下面第一张图
# MAIL_USERNAME = '**********@qq.com'
