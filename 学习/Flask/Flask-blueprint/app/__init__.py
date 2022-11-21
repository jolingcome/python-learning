# init中的脚本是程序运行时都会初始化这里面的功能

#项目的工程结构如下：
#按功能结构来分
"""
project/
    app/
        __init__.py  #初始化app
        static/   #放图片等静态文件
        templates/   #放html页面
            home/
            admin/
        views/  #放一些页面方法。下面的.py文件都是蓝图
            __init__.py
            home.py
            admin.py
        models.py  #放数据库模型
        config.py  #配置文件

    README.md
    requirements.txt
    manage.py  #运行文件，程序入口
"""

#按分区来划分
"""
project/
    app/
        __init__.py
        admin/
            __init__.py
            views.py
            static/
            templates/
        home/
            __init__.py
            views.py
            static/
            templates/
        models.py
        config.py

    README.md
    requirements.txt
    manage.py
"""

from flask import Flask
from .views.index import index_bluePrint
from . import config

def create_app():
    app=Flask(__name__)
    app.config.from_object(config)  #从config文件中导入配置
    app.register_blueprint(index_bluePrint) #注册蓝图

    return app