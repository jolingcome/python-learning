# 当用户提交注册信息的时候，flask会去数据库中进行查询，如果用户名不存在则将用户信息写入sqlite，
# 否则给出无效用户名的错误信息，要求用户重新填写

#Flask连接数据库:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test'
# 其他设置：
#
# # 动态追踪修改设置，如未设置只会提示警告
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# #查询时会显示原始SQL语句
# app.config['SQLALCHEMY_ECHO'] = True
# 名字    备注
# SQLALCHEMY_DATABASE_URI    用于连接的数据库 URI 。例如:sqlite:tmp/test.dbmysql://username:password@server/db


from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo,Length,Email
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.secret_key="test"
#设置数据库URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#使用app作为参数实例化一个SQLAlchemy类的对象
db=SQLAlchemy(app)

#创建会员模型
class Member(db.Model):
    id=db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(45),unique=True)
    email=db.Column(db.String(45))
    password=db.Column(db.String(128))

    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password

#创建数据表,将字段建好
with app.test_request_context(): #用于解决上下文的问题，如果没有此语句就会报错
    db.create_all()

#使用WFT实现表单，自定义一个表单类
class RegisterForm(FlaskForm):
    username=StringField(label="用户名：",validators=[DataRequired()])
    email=StringField(label="邮箱：",validators=[DataRequired(),Email(message='邮箱格式错误')])
    password = PasswordField(label='密码: ', validators=[DataRequired(), Length(6, 16, message='密码格式错误')])
    password2 = PasswordField(label='确认密码: ', validators=[DataRequired(), Length(6, 16, message='密码格式错误'), EqualTo('password', message='密码不一致')])
    submit = SubmitField(label='注册')

@app.route('/',methods=['GET','POST'])
def register():
    register_form=RegisterForm() #实例化表单

    if request.method=="POST":  #前端是post
        if register_form.validate_on_submit(): #在提交按钮后
            username=request.form.get("username")  #request.form.get获取前端表单用户输入的数据
            email=request.form.get("email")
            password=request.form.get('password')

            #判断数据库中是否已经存在相同的用户名
            if Member.query.fliter_by(username=username).all(): #用前端传过来的username查询，有数据表示已经存在
                return 'Invalid username'

            #数据库没有查询到username,构建数据库记录并写入数据库
            member=Member(username=username,email=email,password=password)
            db.session.add(member)
            db.session.commit()
            return 'Reister success'
        else:
            return 'Invalid'

    # 把实例化后的register_form传入到页面register.html中.
    return render_template('register.html', form=register_form)

if __name__=='__main__':
    app.run(host='127.0.0.1',debug=True,port=5002)