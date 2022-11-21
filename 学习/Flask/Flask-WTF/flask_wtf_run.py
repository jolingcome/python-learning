# web表单是web应用程序的基本功能。它是HTML页面中负责数据采集的部件。
# # 表单有三个部分组成：表单标签、表单域和表单按钮。
# # 前面的教程中提到过的用户登录和文件上传的实例中都有表单的身影。

# Flask-WTF是一个Flask扩展，它封装了WTForms。它的优势可以归纳为以下3点
# (1)可以快速定义表单模板
# (2)验证表单数据
# (3) 能够保护所有表单免受跨站请求伪造(CSRF)的攻击

#表单支持的验证方法，
# https://xugaoxiang.com/2020/07/09/flask-10-wtf/

from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo,Length,Email

app=Flask(__name__)
app.secret_key="test"

#使用WTF实现表单，自定义一个表单类
class RegisterForm(FlaskForm):
    username=StringField(label="用户名:",validators=[DataRequired()])
    email=StringField(label="邮箱:",validators=[DataRequired(),Email(message="邮箱格式错误")])
    password=PasswordField(label="密码:",validators=[DataRequired(),Length(6,16,message="密码格式错误")])
    password2=PasswordField(label="确认密码:",validators=[DataRequired(),Length(6,16,message="密码格式错误"),
                                                      EqualTo('password',message='密码不一致')])
    submit=SubmitField(label="注册")

@app.route('/',methods=["GET","POST"])
def register():
    register_form=RegisterForm()

    if request.method=="POST":
        if register_form.validate_on_submit():
            username=request.form.get("username")
            email=request.form.get("email")
            passord=request.form.get("password")
            password2=request.form.get("password2")

            if username=="yangyang" and email=="yangyang@163.com":
                #进入这里就表示表单验证成功
                return 'Register success,username:{},email:{},password:{}'.format(username,email,passord)
            else:
                return "Error"
        else:
            return "Invalid"

    # 把实例化后的register_form传入到页面register.html中
    return render_template('register.html',form=register_form)

if __name__=='__main__':
    app.run(host='127.0.0.1',debug=True,port=5002)
