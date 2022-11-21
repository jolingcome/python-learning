from flask import Flask,request,jsonify
import logging

app=Flask(__name__)
file_path="test.txt"

@app.route('/recall',methods=["POST"])
def recall_back():
    # aa=request.get_data()

    aa=request.json
    print("++++++")
    print(aa)
    write_file(file_path=file_path,content=str(aa))
    # return aa
    return jsonify(aa)

def write_file(file_path,content):
    with open(file_path,'a+',encoding="utf-8") as f :
        f.write(content)
        f.write("\n")




if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port=5004)