#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import *
from threading import Thread
from flask_mail import *
from flask_email import *
#使用线程编程实现异步发送，否则服务就会卡主，如果是web的话在发送完成之前网页是loading状态

app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.qq.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_PASSWORD = 'vbxyiowhpbvfgfge',
    MAIL_USERNAME = '1348065389@qq.com'
))

mail = Mail()
mail.init_app(app)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def SendMail():
    msg = Message('This is a mail from QQ SMTP HOST',sender='1348065389@qq.com',\
                        recipients=["jing_find@163.com"])
    msg.body = 'From QQ'
    msg.html = '<b>Halo the world!</b>'
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return 'ok'

if __name__=="__main__":
    app.run()