# 协程（异步）
# 协程（Co-routine），也可称为微线程，或非抢占式的多任务子例程，一种用户态的上下文切换技术（通过一个线程实现代码块间的相互切换执行）
# https://blog.csdn.net/qq_43380180/article/details/111573642

# #async/aswait
# 步骤：
# #(1) asyncio事件循环（执行协程函数，必须使用事件循环）,下面是步骤
# import asyncio
#
# async def fun1(): #函数前加上async为协程函数
#     print("协程1")
#
# async def fun2():
#     print("协程2")
# task = [fun1(),fun2()] #task为任务列表
# asyncio.run(task) #python3.7不用手动创建事件循环

# #2.注意事项
# #注意：（1）执行协程函数得到协程对象，函数内部代码不会执行
#      # (2) 执行协程函数内部代码，必须把协程对象交给事件循环处理
# # 例：
# import asyncio
# async def main():
#     print("hello")
#     await asyncio.sleep(1)
#     print("world")
# # print(main()) #函数代码不会执行，python3.8会报错,必须带await
# print(asyncio.run(main()))

#3.await 使用
# await+可等待对象（协程对象，Future,Task对象（IO等待））
# await 是等待对象的返回结果，才会继续执行后续代码
import asyncio
import time

async def say_afeter(delay,what):
    await asyncio.sleep(delay)
    print(what)
# async def main():
#     print(f"started at {time.strftime('%X')}")
#     await say_afeter(1,"hello") #执行完成之后，才继续向下执行
#     await say_afeter(2,"world")
#     print(f"finished at {time.strftime('%X')}")
# asyncio.run(main())

#4.异步并发运行协程
#asyncio.create_task()
#(1)asyncio.create_task()作为异步并发运行协程的函数Tasks。
# 将协程添加到asyncio.create_task()中，则该协程将很快的自动计划运行
async def main():
    task1 = asyncio.create_task(
        say_afeter(1,'hello')
    )
    task2 = asyncio.create_task(
        say_afeter(2,'world')
    )
    print(f"started at {time.strftime('%X')}")
    #2个任务同时执行，直到所有任务执行完成
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")
# asyncio.run(main())
# 使用async/await时 会自动创建Future对象。（在此作为了解即可）

# 实例
# (1)使用正常的网络请求
import requests
import time

def result(url):
    res = request_url(url)
    print(url,res)

def request_url(url):
    res = requests.get(url)
    print("\n",res)
    time.sleep(2)
    print("execute_time:",time.time()-start)
    return res

url_list = ["https://www.csdn.net/",
       "https://blog.csdn.net/qq_43380180/article/details/111573642",
       "https://www.baidu.com/",
       ]

# start = time.time()
# print("start_time:",start)
# task = [result(url) for url in url_list]
# endtime = time.time()-start
# print("\nendtime:",time.time())
# print("all_execute_time:",endtime)

# #（2）使用协程
import asyncio
import requests
import time


async def result(url):
    res = await request_url(url)
    print(url, res)


async def request_url(url):
    res = requests.get(url)
    print(url)
    await asyncio.sleep(2)
    print("execute_time:", time.time() - start)
    return res


url_list = ["https://www.csdn.net/",
            "https://blog.csdn.net/qq_43380180/article/details/111573642",
            "https://www.baidu.com/",
            ]
#
# start = time.time()
# print(f"start_time:{start}\n")
#
# task = [result(url) for url in url_list]
# asyncio.run(asyncio.wait(task))
#
# endtime = time.time() - start
# print("\nendtime:", time.time())
# print("all_execute_time:", endtime)

# 注：使用协程时，需要其底层方法实现时就是协程，才会生效，否则协程不生效！
#
# 此处使用的requests底层实现并不是异步，因此使用了time.sleep() 和 asyncio.sleep()模拟放大网络IO时间。
# 异步模块举例：aiohttp-requests、aiofiles、grequests等

# 3. 使用aiofiles: 异步处理文件,与原生的open文件用法一致
# pip install aiofiles

filename=r'sfe_test.txt'
import aiofiles
async def get_text():
    async with aiofiles.open(filename,mode='r', encoding='utf-8') as f :
        contents = await f.read() #读取文件的时候异步
        print(contents)
asyncio.run(get_text())
#aiofiles还支持迭代：
async def get_text_1():
    async with aiofiles.open(filename,mode='r', encoding='utf-8') as f :
        async for line in f:
            print(line)
asyncio.run(get_text_1())
