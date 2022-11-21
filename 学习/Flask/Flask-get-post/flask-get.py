from flask import Flask,request

app=Flask(__name__)

@app.route("/",methods=["GET"])
def index_get():
    username=request.args.get("username")
    password=request.args.get("password")
    if username == "yang" and password == "yang":
        return f"<html><body>Welcome {username}</body></html>"
    else:
        return f"<html><body>Welcome!</body></html>"


if __name__ == '__main__':
    app.run(debug=True)
