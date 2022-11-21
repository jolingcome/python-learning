# easydict能够让我们使用.操作符，就像访问属性attribute那样访问字典dictionary的值。它不是内置模块，可以通过pip进行安装
# pip install easydict

from easydict import EasyDict as edict
aDict = {"id":1, "data":{"name":"xugaoxiang", "sex":"male"}}
#我们将字典aDict传递给EasyDict得到对象e，然后就可以通过e.加上字典中的key值来访问对应的value值了。
e=edict(aDict)
print(e.id)
print(e.data.name)
#可以通过.操作符来给属性赋值
e.name="yangyang"
e.sex="female"
print(e)