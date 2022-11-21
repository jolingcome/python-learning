# 跨域是指，浏览器从服务器A获取的静态资源，包括html、css、javascript，然后在javascript中通过ajax访问服务器B的静态资源或请求。

# w3c组织制定了 [Cross Origin Resource Sharing](https://www.w3.org/TR/cors/) 的规范，简写为CORS，现在这个规范已经被大多数浏览器支持。
#https://xugaoxiang.com/2020/08/26/flask-17-cors/

from flask import Flask,jsonify
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS  #解决跨越问题


USERS = [
    {"name": "zhangsan"},
    {"name": "lisi"},
    {"name": "wangwu"},
    {"name": "zhaoliu"}
]

class Users(Resource):
    def get(self):
        return jsonify(Users)

    def post(self):
        args=reqparse.RequestParser() \
            .add_argument('name',type=str,location='json',required=True,help="名字不能为空") \
            .parse_args()

        self.logger.debug(args)

app = Flask(__name__)
CORS(app)
api=Api(app,default_mediatype="application/json")

api.add_resource(Users,'/users')

app.run(host="0.0.0.0",port=5001,use_reload=True,debug=True)