from app import create_app  #引入init文件中的create_app



if __name__=="__main__":
    app=create_app() #创建好app
    app.run(use_reloader=True,port=5000)  #会运行view中所有蓝图