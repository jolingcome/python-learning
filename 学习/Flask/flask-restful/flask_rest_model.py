# flask-restful扩展通过api.add_resource()方法来添加路由，
# 方法的第一个参数是一个类名，该类继承Resource基类，
# 其成员方法定义了不同的HTTP请求方法的逻辑；
# 第二个参数定义了URL路径。在Users类中，我们分别实现了get、post、delete方法，
# 分别对应HTTP的GET、POST、DELETE请求。

# 另外，flask-restful还提供了argparse，它可以方便地实现对http请求中客户端发送过来的数据进行校验处理，
# 这有点像表单中的验证方法，在实际项目中非常实用。
#
# 程序启动以后，我们访问 http://127.0.0.1:5001/users，GET请求时会给出USERS的内容、
# POST请求时会在USERS中添加一项(如果不存在)并返回USERS更新后的内容。
# DELETE请求则清空USERS并返回空。

# 次用到的dictConfig，主要的区别在于api.add_resource()方法中，
# 使用了参数resource_class_kwargs，然后在Resource子类中的构造函数__init__，
# 将日志记录器获取到，后面就可以在各个处理方法中使用了。再次使用postman发起POST请求，
# 可以看到debug.log是这个样子的


import logging.config
from flask import Flask,jsonify
from flask_restful import Api,Resource,reqparse



#配置logging.config
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "info.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "errors.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8",
            },
            "debug_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "debug.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "my_module": {"level": "ERROR", "handlers": ["console"], "propagate": "no"}
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["error_file_handler", "debug_file_handler"],
        },
    }
)

USERS=[
    {"name":"zhangsan"},
    {"name":"lisi"},
    {"name":"wangwu"},
    {"name":"zhaoliu"}
]

class Users(Resource):
    def __init__(self,**kwargs):
        self.logger=kwargs.get("logger")

    def get(self):
        return jsonify(USERS)

    def post(self):
        #reqparese是用于校验的，RequestsParser是对传过来的请求进行校验
        args=reqparse.RequestParser() \
            .add_argument('name',type=str,location="json",required=True,help="名字不能为空") \
            .parse_args()

        self.logger.debug(args)

        if args["name"] not in USERS:
            USERS.append({"name":args["name"]})
        return jsonify(USERS)

    def delete(self):
        USERS=[]
        return jsonify(USERS)


class UserId(Resource):
    def __init__(self,**kwargs):
        self.logger=kwargs.get("logger")

    def get(self,userid):
        return jsonify({
            "name":USERS[int(userid)].get("name")
        })

app=Flask(__name__)
api=Api(app,default_mediatype="application/json")

api.add_resource(Users,'/users',resource_class_kwargs={
    "logger":logging.getLogger('/Users')
})

api.add_resource(UserId,'/user/<userid>',resource_class_kwargs={
    "logger":logging.getLogger('/UserId')
})

app.run(host='0.0.0.0',port=5001,use_reloader=True,debug=True)
