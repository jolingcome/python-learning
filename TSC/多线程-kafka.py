#先写入队列，然后再写入多进程。
# 注意事项：1.kafka连接要放外面，只连接一次和关闭一次，放在with ThreadPoolExecutor 外面，避免进程开销。
#          2. 写入消息队列时，用全局变量id_queue，后面直接用此变量就行，因为是直接写入全局变量，所以fake_date不用return
#          3. 队列一次性写入，然后多进程可以快速读取。如果队列里的数据少，进程读取快，也会影响到写入的速度。
#读取json数据
import json
import time
import random
import string
from kafka import KafkaProducer,KafkaConsumer
from kafka.errors import KafkaError

from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
from queue import Queue
import datetime

from functools import wraps

file_start=r"D:\代码\python\TSC\start"
file_end=r"D:\代码\python\TSC\end"
id_queue = Queue(3000)

def read_json(file_path):
    with open(file_path,"r",encoding="utf8") as f:
        row_data=json.load(f)
        # print(row_data)
        return row_data
# print(read_json(file_start))

def get_time():
    t=time.time()
    return int(round(t*1000))
# print(get_time())

def rand(bits):
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set
    value_set = "".join(random.sample(total_set, bits))
    return value_set


# print(object_id)

def start_data(file_path,object_id):
    start_data1=read_json(file_path)
    # print(start_data1["associationObjects"])
    for i in start_data1["associationObjects"]:
        i["objectId"]=object_id
    capturedTime=get_time()
    time.sleep(0.1)
    start_data1["capturedTime"]=capturedTime
    createTime=get_time()
    start_data1["createdTime"]=createTime
    time.sleep(0.2)
    receivedTime=get_time()
    start_data1["receivedTime"]=receivedTime
    return start_data1



def end_data(file_path,object_id):
    end_data1=read_json(file_path)
    capturedTime=get_time()
    time.sleep(0.1)
    end_data1["capturedTime"]=capturedTime
    time.sleep(0.2)
    receivedTime=get_time()
    end_data1["receivedTime"]=receivedTime
    end_data1["objectId"]=object_id
    return end_data1

# print(end_data(file_end))


def kafkaProduce_34(ip, topicName, msg, port=9092):
    producer = KafkaProducer(sasl_mechanism="PLAIN",
                             security_protocol='SASL_PLAINTEXT',
                             sasl_plain_username="admin",
                             sasl_plain_password="KmwWTNGhmlQGvGv",
                             # bootstrap_servers=[f"172.20.25.34:9092"])
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                             bootstrap_servers=[f"{ip}:{port}"])
    a = producer.send(topicName, key=None, value=msg)
    print(a.get(timeout=10000))
    producer.close()
# aa=kafkaProduce_34(ip="172.20.25.34",topicName="AsyncEvent",msg=start_data,port=9092)
# print(aa)


def fake_data(file_start_path,file_end_path,num=10):
    id_queue.queue.clear()
    for i in range(num):
        object_id = rand(8) + "-" + rand(3) + "-" + rand(4) + "-" + rand(4) + "-" + rand(12)
        # print(object_id)
        start_data_result=start_data(file_start_path,object_id)
        end_data_result = end_data(file_end_path, object_id)
        id_queue.put(start_data_result)
        id_queue.put(end_data_result)




# def defake_request_multi_pool(thread_num=5,data_num=2):
#     fake_data(file_start_path=file_start, file_end_path=file_end,num=data_num)
#     startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#     print(startTime)
#     # print(id_queue.qsize())
#     with ThreadPoolExecutor(max_workers=thread_num,thread_name_prefix='kafkf_reqeust') as t:
#         while id_queue.qsize() > 0:
#             print(f'***********start********')
#             for i in range(0, thread_num):
#                 feature = t.submit(kafkaProduce_34(ip="172.20.25.34", topicName="AsyncEvent", msg=id_queue.get(), port=9092))
#             print(f'***********end********')
#             print(id_queue.qsize())
#
#     endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#     print(endTime)
#
# test=defake_request_multi_pool(thread_num=4,data_num=8)
# print(test)


def defake_request_multi_pool(thread_num=5, data_num=2):
    fake_data(file_start_path=file_start, file_end_path=file_end, num=data_num)
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(startTime)
    # print(id_queue.qsize())
    with ThreadPoolExecutor(max_workers=thread_num, thread_name_prefix='kafkf_reqeust') as t:
        futures = []
        while id_queue.qsize() > 0:
            print(f'***********start********')
            for i in range(0, thread_num):
                feature = t.submit(
                    kafkaProduce_34(ip="172.20.25.34", topicName="AsyncEvent", msg=id_queue.get(), port=9092))
                futures.append(feature)
            print(f'***********end********')
            print(id_queue.qsize())

        for future in futures:
            print(future.result())
    endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(endTime)

test=defake_request_multi_pool(thread_num=5,data_num=10)
print(test)











