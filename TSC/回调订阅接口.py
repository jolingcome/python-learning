from flask import Flask,request
import logging

app=Flask(__name__)
file_path="test.txt"

@app.route('/recall',methods=["POST"])
def recall_back():
    aa=request.get_data()
    print(aa)
    write_file(file_path=file_path,content=str(aa))
    return aa

def write_file(file_path,content):
    with open(file_path,'wt',encoding="utf-8") as f :
        f.writelines(content)




if __name__=='__main__':
    app.run(host='127.0.0.1',debug=True,port=5002)