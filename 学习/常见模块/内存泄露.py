#1. python 自带的机制会自动释放不被引用的内存空间，用sys.getrefcount(a)查看引用的次数
#2. 手动释放方法步骤：（1）del a (a是引用);（2）gc.collect()
#3. 循环引用查看是否会引起内存泄露：objgraph

#【查看引用次数（sys.getrefcount（）调用次方法会算一次）】
import os
import psutil

#1.显示python程序占用内存的大小:程序结束,引用被释放，内存释放
def show_memory_info(hint):
    pid=os.getpid()
    p=psutil.Process(pid)

    info=p.memory_full_info() #获取内存大小
    memory=info.uss / 1024. / 1024
    print(f"{hint}memory used:{memory}MB")
def func():
    show_memory_info("initial")
    # global a #全局变量程序结束不会释放
    a=[i for i in range(10000)]
    show_memory_info('after a created')
    # return a #return返回然后在主程序里面接收，即b=func(),也不会释放内存,

b=func()
show_memory_info('finished')

#2.python的内部引用机制
import sys
# a=[]
# #2次引用：1次来自a,一次来自getrefcount
# print(sys.getrefcount(a))

#四次引用：变量a,func(a)参数a,getrefcount调用一次，func(a)函数调用一次
# a=[]
# def func(a):
#     print(sys.getrefcount(a))
# func(a)

# #8次引用：变量a,b,c,d,e,f,g各1次，getrefcount 1次
# a=[]
# b=a
# c=b
# d=b
# e=c
# f=e
# g=d
# print(sys.getrefcount(a))

# #3.手动释放内存
# print("========================= 手动垃圾回收 =============================")
# import gc
# show_memory_info("initial")
# a=[i for i in range(10000)]
# show_memory_info('after a created')
# #手动启用垃圾回收
# del a
# gc.collect()
# show_memory_info('finish')
# print(a)


#4.循环引用查看是否会引起内存泄露：objgraph
# #a,b一开始占用的空间不是很大，但经过长时间的运行，python所占用的内存会越来越大。这种情况会想到gc.collect解决
# print("========================= 循环引用，即相互引用 =============================")
# import gc
# def func_1():
#     show_memory_info("initial")
#     a=[i for i in range(10000)]
#     b = [i for i in range(10000)]
#     show_memory_info('after a,b created')
#     a.append(b)
#     b.append(a)
# func_1()
# # gc.collect() #可以调用gc.collect()来启动垃圾回收
# show_memory_info('finished')
#使用工具objgraph看可视化引用关系
import objgraph
a=[1,2,3]
b=[4,5,6]
a.append(b)
b.append(a)
objgraph.show_refs([a],filename='sample-graph.png')
# objgraph.show_backrefs([a])


