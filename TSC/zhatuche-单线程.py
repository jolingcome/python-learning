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


from kafka import KafkaClient

from kafka import KafkaProducer

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


def fake_data(file_start_path,file_end_path,num=10):
    data_result=[]
    # id_queue.queue.clear()
    for i in range(num):
        object_id = rand(8) + "-" + rand(3) + "-" + rand(4) + "-" + rand(4) + "-" + rand(12)
        # print(object_id)
        start_data_result=start_data(file_start_path,object_id)
        end_data_result = end_data(file_end_path, object_id)
        data_result.append(start_data_result)
        data_result.append(end_data_result)
    return data_result
        # id_queue.put(start_data_result)
        # id_queue.put(end_data_result)
data=fake_data(file_start_path=file_start, file_end_path=file_end,num=500)
print(data)


def producer_1():
    producer = KafkaProducer(sasl_mechanism="PLAIN",
                             security_protocol='SASL_PLAINTEXT',
                             sasl_plain_username="admin",
                             sasl_plain_password="KmwWTNGhmlQGvGv",
                             # bootstrap_servers=[f"172.20.25.34:9092"])
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                             bootstrap_servers=["172.20.25.34:9092"])
    return producer
def send_data(topic):
    producer_0 = producer_1()
    try:
        for i in data:
            # print(i)
            a = producer_0.send(topic=topic, key=None,value=i)
            print(a.get(timeout=10000))
    except KafkaError as e:
        print(e)
    finally:
        producer_0.close()


if __name__=='__main__':
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(startTime)
    send_data(topic='AsyncEvent')
    endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(endTime)







