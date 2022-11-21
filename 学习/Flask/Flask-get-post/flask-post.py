from flask import Flask,request

app=Flask(__name__)

@app.route("/post",methods=["POST"])
def index_get():
    username=request.form["username"]
    password=request.form["password"]
    if username == "yang" and password == "yang":
        return f"<html><body>Welcome {username}</body></html>"
    else:
        return f"<html><body>Welcome!</body></html>"


if __name__ == '__main__':
    app.run(debug=True)
