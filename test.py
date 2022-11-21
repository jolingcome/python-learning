import requests
#1.pdb是用于调试
#import pdb
#pdb.set_trace()

#2.cProfile进行性能分析

# import cProfile
# import threading
# url="https://firebasestorage.googleapis.com/v0/b/driver-app-547b8-hucue-fr/o/20220116%2F012d7257-6f6c-42d5-a729-8b398e5dddd6_1642321622532.jpg?alt=media&token=ee589110-7476-46bd-85d0-6e61f4b63b5b"
# # file_path=r"‪C:/yangling2/桌面/医院归档图片.txt"
# file_path="C:/yangling2/桌面/医院归档图片.txt"
# save_path=r"C:/yangling2/桌面/医疗/"
# def read_txt(file_path):
#     with open(file_path,mode="r",encoding="utf-8") as f:
#         result=f.read()
#         result_01=result.split("/n")
#         print(result_01)
#         result_new=result_01[-1]
#         print(result_new)
#
#         with open(result_01,mode="w",encoding="utf-8") as p:
#             p.write(save_path+result_new)
#
#
#
# a=read_txt(file_path)
# print(a)
#
# def get_name(url):
#     url = url.split("/")
#     name = url[-1].split("?")[0]
#     return name
#
# def get_pic(url):
#     proxy = {"http":"http://proxy.sensetime.com:3182","https":"172.16.1.135:3128"}
#     name=get_name(url)
#     r = requests.get(url,proxies=proxy)
#     with open(file=name,mode="wb") as f:
#         f.write(r.content)
#
# result=get_pic(url=url)
#
#
# #改进性能的办法，我们可以用字典来保存计算过的结果，防止重复。
# def memoize(f):
#     memo={}
#     def helper(x):
#         if x not in memo:
#             memo[x]=f(x) #f是函数
#         return memo[x]
#     return helper
#
# @memoize
# def fib(n):
#     if n==0:
#         return 0
#     elif n==1:
#         return 1
#     else:
#         return fib(n-1)+fib(n-2)
#
# def fib_seq(n):
#     res=[]
#     if n>0:
#         res.extend(fib_seq(n-1))
#     res.append(fib(n))
#     return res
# result=fib_seq(30)
# cProfile.run('result')
#
#
# #setattr为模块动态添加属性.相当于将函数加别名
# import sys
# thismodule=sys.modules[__name__]
#
# def addfunc():
#     a=1
#     b=2
#     c=a+b
#     print("c value is:", c)
#
#
# def subfunc(a, b):
#     c = a - b
#     print("a - b is:", c)
#
# setattr(thismodule,"add",addfunc)
# setattr(thismodule, "sub", subfunc)


#闭包：内部函数调用外部函数变量
#闭包的使用情况：多个变量，外部变量需要固定，只改变内部变量时使用（如计算器，a*x+b=y大多少情况下a,b固定，只要改变x即可）
#闭包格式：
# def out_fun():
#     def in_fun():
#         return #内部函数的返回值
#     return in_fun #返回内部函数名，后面函数调用时引用
# 例1：写入计数器
def count():
    cnt=[0]
    def add(b):
        return cnt[0]+b
    return add
#例2：a*X+b=y计算Y,a,b传一次后固定
def y_fic(a,b):
    def add(x):
        return a*b+x
    return add
#函数调用
fun1=y_fic(2,3)
fun2=fun1(3)
print(fun2)
#继续传入x
fun3=fun1(4)
print(fun3)






