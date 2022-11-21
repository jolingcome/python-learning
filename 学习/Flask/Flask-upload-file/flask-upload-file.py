# 在Flask中进行文件上传，需要在通过html中的form表单，而且需要设置enctype=multipart/form-data

# 注意到success方法中，只处理POST请求，并从请求对象中的files获取到文件的内容，调用save保存文件，
# # 渲染网页时，将文件名传递过去，文件名会在success.html中显示

from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/upload_file')
def upload_file():
    return render_template('flask-upload-file.html')

@app.route('/success',methods=['post'])
def success():
    if request.method == 'POST':
        f=request.files['file']
        f.save(f.filename)
        return render_template('flask-upload-file-success',name=f.filename) #渲染页面时，将f.filename传入

if __name__ == '__main__':
    app.run(debug=True)
