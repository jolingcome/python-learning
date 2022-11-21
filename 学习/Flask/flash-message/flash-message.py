#在Flask中，使用flash message(闪现消息)，具体使用的方法是flash()
# flash(message, category)

# message: 具体的消息内容
# # category: 可选参数，表示消息类型，比如错误、警告等
# 在视图函数中发送了消息，自然的，就需要在模板文件中取出消息，我们使用方法get_flashed_message
# get_flashed_messages(with_categories, category_filter)
# with_categories: 消息类型，与上面的flash匹配
# category_filter: 过滤条件

from flask import Flask,render_template,request,redirect,url_for,flash
app=Flask(__name__)
app.secret_key="test"

@app.route("/")
def index():
    return render_template("index-flash.html")

@app.route("/login",methods=["GET","POST"])
def login():
    error=None
    if request.method=="POST":
        if request.form["email"] != "yangyang@email.com" or request.form['password'] != 'test':
            error="Invalid account."
        else:
            flash("Login successfully")
            return redirect(url_for("index"))
    return render_template("login.html",error=error)

if __name__=='__main__':
    app.run(host='127.0.0.1',debug=True,port=5001)