#注意事项：
# （1）html必须放在templates目录下，要不然flask通过jinjia找不到
# （2）app.run 端口开开了要关掉，要不然下个脚本就不能用此端口

from flask import Flask,render_template,request,redirect,url_for

app=Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/validate',methods=['POST'])
def validate():
    if request.method=='POST' and request.form['email']=='yangyang@163.com' and request.form["password"]=="yangyang":
        return redirect(url_for('success'))
    return redirect(url_for('login'))

@app.route('/success')
def success():
    return 'Login sucessfully'

if __name__=='__main__':
    app.run(host='127.0.0.1',debug=True,port=5001)
