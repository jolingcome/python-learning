# 通过scripts目录下的dbInitialize.py脚本文件创建初始数据库表并插入一条数据，
# 用户名是admin@gmail.com，密码是字符串123456经过sha256加密后的数据，默认用户是激活状态

import hashlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1qaz2wsx@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app)

#创建表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self,username=None,password=None,active=True):
        self.username=username
        self.password=password
        self.active=True

try:
    db.create_all()

    hash_password=hashlib.sha256(b"123456").hexdigest()
    user=User(username="admin@gmail.com",password=hash_password)
    db.session.add(user)
    db.session.commit()
except:
    pass

db.session.close()