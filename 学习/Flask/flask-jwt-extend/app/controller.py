# 重点来看看用户登录部分的后端实现，还是RESTful API，这里提供一个POST方法，接收客户端发送过来的JSON数据，解析后得到用户名及加密后的密码，
# 如果用户名存在于我们的数据库中且密码相符，调用flask_jwt_extended的create_access_token方法生成对应的token，注意到create_access_token的参数部分，
# 我们传递的是username。flask_jwt_extended还提供了方法get_jwt_identity，可以从token中获取到username，这点在实际项目中非常有用。

from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token,jwt_required
from app.models import User
from app import jwt

