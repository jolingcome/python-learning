from flask import Blueprint

index_bluePrint = Blueprint('index',__name__)  #实例化蓝图

@index_bluePrint.route('/')  #使用蓝图
def index():
    return "Hello blueprint"

