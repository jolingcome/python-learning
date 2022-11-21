# -*- coding: UTF-8 -*-
"""
# rs勿忘初心
"""
from flask import Flask
from flask_restful import Api
from flask import jsonify, request
from flask import make_response

app = Flask(__name__)
app.config["DEBUG"] = True

api = Api(app)


@app.route('/health', methods=["GET", "POST"])
def health():
    """
    # 健康检查接口
    :return:
    """
    result = {
        "code": "200",
        "message": "success",
        "data": "green"
    }

    return make_response(jsonify(result))


@app.route('/open_ability', methods=["POST"])
def open_ability():
    """
    # 开放能力接口
    :return:
    """
    request_data = request.json

    # 默认值
    env_name = "sandbox"
    if "param_dict" in request_data and "env_name" in request_data["param_dict"]:
        env_name = request_data["param_dict"]["env_name"]

    result = {
        "code": 0,
        "msg": "{} 环境检查符合预期, 可以正常使用".format(env_name),
        "need_push": 1,
        "status": "success"
    }

    return make_response(jsonify(result))


if __name__ == "__main__":
    # 启动服务
    app.run(host="0.0.0.0", port=8080, debug=False)