#Session跟上面的Cookie非常类似，只不过Session是存储在服务器端的，在实际场景中经常遇到的登录失效，就是因为Session在起作用。
# 在Flask中，使用session对象来存放键值对。需要注意的是，使用Session需要设置app.secret_key
# make_response 构造响应体，如果是直接响应返回到html则直接用render_template

from flask import Flask,render_template,make_response,jsonify



app=Flask(__name__)
# app.secret_key="test"

# @app.route('/session',methods=['GET'])
# def session():
#     resp=make_response("<html><body>Session.<a href='/getValue'>Get Value</a></body></html>")
#     session["name"]="yangyang"
#     return resp

# @app.route('/getValue')
# def getValue():
#     if 'name' in session:
#         name=session["name"]
#         return render_template('get-session.html', name=name)


## 构造响应体的方法：
# http://t.zoukankan.com/leijiangtao-p-4162829.html
#（1） make_response 来构造响应体
  # 使用make_response 来构造响应信息（从flask中导入make_response）
  #         resp =  make_response("响应体")
  #         resp.status = "状态码，可以是自定义的状态码"
  #         resp.headers["键"] = "值"   #  通过字典的形式设置响应头
@app.route("/index_get_response")
def index_get_response():
    resp = make_response("index page2") # 响应体数据
    resp.status = "999 itcast" # 状态码
    resp.headers["City"] = "ShangHai" # 通过字典的形式添加响应头
    return resp

#（2）给前端返回json数据：
     # 1. 通过传统的方式，先构造一个字典，然后经过json模块转化为字符串，视图函数返回字符串以及修改响应头的类型接口
     #  2.通过flask中的 jsonify来进行返回，有两种方式
    #  第一种是把构造好的字典直接传进去返回即可   return jsonify(构造的字典)
     # 第二种是直接在jsonify() 里面进行构造      return jsonify(键=值,键=值) ，其效果是一样的
@app.route("/index_jsonfy")
def index_jsonfy():
    """向前端返回json类型的数据"""
    data = {
        "name": "python",
        "age": 18
    }
    """
        传统的方式去传递
        # json.dumps(字典)  将Python的字典转换为json的字符串
        # json.loads(字符串)  将字符串转换为Python中的字典
        json_str = json.dumps(data)
        # 改变，响应头的类型
        return json_str,200,{"Content-Type":"application/json"}
    """
    '''
        jsonify()的使用
        1.jsonify()帮助转为json数据，并设置响应头 Content-Type 为 application/json
        2. 可以不用提前构造好字典，直接返回,结果是一样的
            return jsonify(City="Beijing",age=20)
    '''
    return jsonify(data)

# if __name__ == '__main__':
#     app.run(debug=True)