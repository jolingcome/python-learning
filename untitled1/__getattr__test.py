#__getattr__用于不存在的属性
class Test(object):
    def __init__(self, name):
        self.name = name

    def __getattr__(self, value): #获取属性值
        if value == 'address': #test.address表示test对象的属性是address.故返回"china";下面的test.address='Anhui',它的属性address的值是''
            return 'China'

# 如果是调用了一个类中未定义的方法，则__getattr__也要返回一个方法，例如：
# class Test(object):
#     def __init__(self, name):
#         self.name = name
#
#     def __getattr__(self, value):
#         return len



if __name__ == "__main__":
    test = Test('letian')
    print(test.name)
    print(test.address)
    test.address = 'Anhui'
    print(test.address)
    # print(test.getlength('letian'))