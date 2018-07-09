from database import db
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(64),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    # confirmed = db.Column(db.Boolean, default=False)

    # def generate_confirmation_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'confirm': self.id}).decode('utf-8')

    # def confirm(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True


    # def __init__(self,*args,**kwargs):
    #     email = kwargs.get('email')
    #     username = kwargs.get('username')
    #     password = kwargs.get('password')

    #     self.email = email
    #     self.username = username
    #     self.password = generate_password_hash(password)

class Comments(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    # now()获取的是服务器第一次运行的时间
    # now就是每次创建一个模型的时候，都获取当前的时间
    create_time = db.Column(db.DateTime,default=datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User',backref=db.backref('comment'))

		# #创建电影表
		# self.cursor.execute("drop table if exists films")
		# sql="""create table films (
		# 	id int(32) not null auto_increment,
		# 	link varchar(255),
		# 	name varchar(255) not null,
		# 	picture varchar(255),
		# 	type varchar(255),
		# 	place varchar(255),
		# 	length varchar(255),
		# 	introduction varchar(255),
		# 	primary key(id)
		# 	)ENGINE=InnoDB DEFAULT CHARSET=utf8"""

class Film(db.Model):
    __tablename__='film'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    score=db.Column(db.String(64),nullable=False)
    name=db.Column(db.String(64),nullable=False)
    pic=db.Column(db.String(64),nullable=False)
    tags=db.Column(db.String(64),nullable=False)
    area=db.Column(db.String(64),nullable=False)
    time=db.Column(db.String(64),nullable=False)
    introduction=db.Column(db.String(1000),nullable=False)
    show_id=db.Column(db.String(64),nullable=False)

    # def __init__(self,*args,**kwargs):
    #         show_id = kwargs[0]
    #         name = kwargs[1]
    #         pic = kwargs[2]
    #         tag = kwargs[3]
    #         area = kwargs[4]
    #         score = kwargs[5]
    #         time = kwargs[6]
    #         intro = kwargs[7]
            

# show_id = show_id,name = name,pic = pic,tags=tag,area=area,time=time,intro=intro,score=score

