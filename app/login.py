#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,session,g,redirect,url_for,render_template_string
from werkzeug.security import generate_password_hash,check_password_hash
import config
from models import User,Film
from database import db
import json
from flask import flash
from functools import wraps
from flask import session,redirect,url_for

# 登录限制的装饰器
def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper

# from spider2 import ListSpider
# spider=ListSpider()
# filmlist= spider.get_all_movie_infos(1)

app=Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# def add_films():
#     for kwargs in filmlist:
#         show_id = kwargs[0]
#         name = kwargs[1]
#         pic = kwargs[2]
#         tag = kwargs[3]
#         area = kwargs[4]
#         score = kwargs[5]
#         time = kwargs[6]
#         intro = kwargs[7] 
#         film=Film(show_id = show_id,name = name,pic = pic,tags=tag,area=area,time=time,intro=intro,score=score)
#         db.session.add(film)
#         db.session.commit()

@app.route('/')
def films():
    # add_films()
    return redirect(url_for('login'))

# @app.route('/')
# def home():
#     return render_template('login.html')

@app.route('/login/',methods=['POST','GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        print(password)
        user = User.query.filter(User.email == email).first()
        if user and check_password_hash(user.password,password):
            session['user_id'] = user.id
            #如果想在31天内都不需要登录
            # session.permanent = True
            return redirect(url_for('index'))
        else:
            flash("请重新输入密码")
            return redirect(url_for('login'))
            
        
@app.route('/index/',methods=['POST','GET'])
@login_required
def index():
    if request.method=='GET':
        # film=Film()
        # for i in range(0,12):
        #     film.append(Film.query.filter(Film.id==i)).first()
        return render_template('index.html')
    else:
        pass
 
@app.route('/signup/',methods=['POST','GET'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # 邮箱验证，如果被注册了，就不能再注册了
        user1 = User.query.filter(User.email == email).first()
        if user1:
            #邮箱已被注册
            return u'该邮箱已被注册，请更换邮箱！'
        else:
            # if user2:
            #     #
            #     return u'该用户名已被注册，请更换用户名！'
            # else:
                # password1要和password2相等才可以
            if password1 != password2:
                return u'两次密码不相等，请核对后再填写！'
            else:
                user = User(email=email,username=username,password=generate_password_hash(password1))
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登录的页面
                return redirect(url_for('login'))

if __name__=='__main__':
    app.run()
