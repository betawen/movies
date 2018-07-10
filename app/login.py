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


app=Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 登录限制的装饰器
def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user

@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}

# from spider2 import ListSpider
# spider=ListSpider()
# filmlist= spider.get_all_movie_infos(1)

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
def welcome():
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
            return render_template('login.html')
            
        
@app.route('/index/',methods=['POST','GET'])
@login_required
def index():
    context={
        "movies": Film.query.limit(36).all()
    }
    return render_template('index.html',**context)
 

@app.route('/movies/',methods=['GET','POST'])
@login_required
def movies():
    # if request.form.get('change'):
    #     context={
    #     "movies": Film.query.limit(24,36).all()
    # }
    if request.method=='POST':
        print('1')
    else:
        pass
    if request.values.get('change'):
        print(a)
        context={
        "movies": Film.query.all()[5:8]
    }
        return render_template('index.html',**context)
    else:
        return redirect(url_for('index'))
            

@app.route('/movie/',methods=['GET','POST'])
@login_required
def filmtest():
    if request.method=='GET':
        context={
        "movies": Film.query.limit(36).all()
        }
        return render_template('film.html')
    else:
    # movie1 = User.query.filter(Film.name == name).first()
        context={
        "movies": Film.query.limit(36).all()
        }
        # return render_template('film.html',**context)
        return {"hh":"dd"}


@app.route('/register/',methods=['POST','GET'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        email = request.values.get('email')
        print(email)
        username = request.form.get('username')
        print(username)
        password1 = request.form.get('password1')
        print(password1)
        password2 = request.form.get('password2')
        print(password2)
        sex=request.values.get('Sex')
        print(sex)
        # 邮箱验证，如果被注册了，就不能再注册了
        user1 = User.query.filter(User.email == email).first()
        if user1:
            #邮箱已被注册
            flash('该邮箱已被注册，请更换邮箱！')
            return render_template('register.html',myuser=user1) 
        else:
            user = User(email=email,username=username,password=generate_password_hash(password1),sex=sex)
            db.session.add(user)
            db.session.commit()
            # 如果注册成功，就让页面跳转到登录的页面
            return redirect(url_for('login'))

@app.route('/store/')
def store():
    f1 = open('film.json', 'a')
    filmlist=[]
    for film in Film.query.all():
        f={
            "name":film.name,
            "show_id":film.id,
            "tags":film.tags,
            "time":film.time,
            "intro":film.introduction,
            "pic":film.pic,
            "area":film.area,
            "score":film.score
        }
        filmlist.append(f)
    print(filmlist)
    return "finish"

if __name__=='__main__':
    app.run()
