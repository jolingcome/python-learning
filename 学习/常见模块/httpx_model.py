#https://xugaoxiang.com/category/python/modules/
from flask import Flask,jsonify,request
from flask_restful import Api,Resource,reqparse

USERS = [
    {"name": "zhangsan"},
    {"name": "lisi"},
    {"name": "wangwu"},
    {"name": "zhaoliu"}
]

class Users(Resource):

    def get(self):
        return jsonify(USERS)

    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('name', type=str, location='json', required=True, help="名字不能为空") \
            .parse_args()

        if args['name'] not in USERS:
            USERS.append({"name": args['name']})

        return jsonify(USERS)

    def delete(self):
        USERS = []
        return jsonify(USERS)

class UserId(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('age', type=int)

    def get(self, userid):
        datas = self.parser.parse_args()

        return jsonify(
            {"name": USERS[int(userid)].get('name'), "age": datas.get('age')}
        )

    def post(self, userid):
        file = request.files['file']
        file.save('flask_file.txt')

        return jsonify({
            'msg' : 'success'
        })

app = Flask(__name__)
api = Api(app, default_mediatype="application/json")

api.add_resource(Users, '/users')
api.add_resource(UserId, '/user/<userid>')

app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)