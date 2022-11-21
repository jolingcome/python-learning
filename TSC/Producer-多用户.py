#!/usr/bin/env python
# Author: rex.cheny
# E-mail: rex.cheny@outlook.com
 
import time
import random
import sys
 
from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError
import json
import datetime
from concurrent.futures import ThreadPoolExecutor

"""
KafkaProducer是发布消息到Kafka集群的客户端，它是线程安全的并且共享单一生产者实例。生产者包含一个带有缓冲区的池，
用于保存还没有传送到Kafka集群的消息记录以及一个后台IO线程，该线程将这些留在缓冲区的消息记录发送到Kafka集群中。
"""
 
"""
KafkaProducer构造函数参数解释
    - acks 0表示发送不理睬发送是否成功；1表示需要等待leader成功写入日志才返回；all表示所有副本都写入日志才返回
    - buffer_memory 默认33554432也就是32M，该参数用于设置producer用于缓存消息的缓冲区大小，如果采用异步发送消息，那么
                    生产者启动后会创建一个内存缓冲区用于存放待发送的消息，然后由专属线程来把放在缓冲区的消息进行真正发送，
                    如果要给生产者要给很多分区发消息那么就需要考虑这个参数的大小防止过小降低吞吐量
    - compression_type 是否启用压缩，默认是none，可选类型为gzip、lz4、snappy三种。压缩会降低网络IO但是会增加生产者端的CPU
                       消耗。另外如果broker端的压缩设置和生产者不同那么也会给broker带来重新解压缩和重新压缩的CPU负担。
    - retries 重试次数，当消息发送失败后会尝试几次重发。默认为0，一般考虑到网络抖动或者分区的leader切换，而不是服务端
              真的故障所以可以设置重试3次。
    - retry_backoff_ms 每次重试间隔多少毫秒，默认100毫秒。
    - max_in_flight_requests_per_connection 生产者会将多个发送请求缓存在内存中，默认是5个，如果你开启了重试，也就是设置了
                                            retries参数，那么将可能导致针对于同一分区的消息出现顺序错乱。为了防止这种情况
                                            需要把该参数设置为1，来保障同分区的消息顺序。
    - batch_size 对于调优生产者吞吐量和延迟性能指标有重要的作用。buffer_memeory可以看做池子，而这个batch_size可以看做池子里
                 装有消息的小盒子。这个值默认16384也就是16K，其实不大。生产者会把发往同一个分区的消息放在一个batch中，当batch
                 满了就会发送里面的消息，但是也不一定非要等到满了才会发。这个数值大那么生产者吞吐量高但是性能低因为盒子太大占用内存
                 发送的时候这个数据量也就大。如果你设置成1M，那么显然生产者的吞吐量要比16K高的多。
    - linger_ms 上面说batch没有填满也可以发送，那显然有一个时间控制，就是这个参数，默认是0毫秒，这个参数就是用于控制消息发送延迟
                多久的。默认是立即发送，无需关系batch是否填满。大多数场景我们希望立即发送，但是这也降低了吞吐量。
    - max_request_size 最大请求大小，可以理解为一条消息记录的最大大小，默认是1048576字节。
    - request_timeout_ms  生产者发送消息后，broker需要在规定时间内将处理结果返回给生产者，那个这个时间长度就是这个参数
                          控制的，默认30000，也就是30秒。如果broker在30秒内没有给生产者响应，那么生产者就会认为请求超时，并在回调函数
                          中进行特殊处理，或者进行重试。
 
"""
class Producer(object):
    def __init__(self, KafkaServerList=['127.0.0.1:9092'], ClientId="Procucer01", Topic='Test'):
        self._kwargs = {
            "bootstrap_servers": KafkaServerList,
            "client_id": ClientId,
            "acks": 1,
            "buffer_memory": 33554432,
            'compression_type': None,
            "retries": 3,
            "batch_size": 1048576,
            "linger_ms": 100,
            "key_serializer": lambda m: json.dumps(m).encode('utf-8'),
            "value_serializer": lambda m: json.dumps(m).encode('utf-8'),
            'sasl_mechanism': "PLAIN",
            'security_protocol': 'SASL_PLAINTEXT',
            'sasl_plain_username': "admin",
            'sasl_plain_password': "KmwWTNGhmlQGvGv"
        }
        self._topic = Topic
        try:
            self._producer = KafkaProducer(**self._kwargs)
        except Exception as err:
            print(err)
 
 
    def _onSendSucess(self, record_metadata):
        """
        异步发送成功回调函数，也就是真正发送到kafka集群且成功才会执行。发送到缓冲区不会执行回调方法。
        :param record_metadata:
        :return:
        """
        print("发送成功")
        print("被发往的主题：", record_metadata.topic)
        print("被发往的分区：", record_metadata.partition)
        print("队列位置：", record_metadata.offset)  # 这个偏移量是相对偏移量，也就是相对起止位置，也就是队列偏移量。
 
 
    def _onSendFailed(self):
        print("发送失败")
 
 
    def sendMessage(self, value=None, partition=None):
        if not value:
            return None
 
        # 发送的消息必须是序列化后的，或者是字节
        # message = json.dumps(msg, encoding='utf-8', ensure_ascii=False)
 
        kwargs = {
            "value": value, # value 必须必须为字节或者被序列化为字节，由于之前我们初始化时已经通过value_serializer来做了，所以我上面的语句就注释了
            "key": None,  # 与value对应的键，可选，也就是把一个键关联到这个消息上，KEY相同就会把消息发送到同一分区上，所以如果有这个要求就可以设置KEY，也需要序列化
            "partition": partition # 发送到哪个分区，整型。如果不指定将会自动分配。
        }
 
        try:
            # 异步发送，发送到缓冲区，同时注册两个回调函数，一个是发送成功的回调，一个是发送失败的回调。
            # send函数是有返回值的是RecordMetadata，也就是记录的元数据，包括主题、分区、偏移量
            future = self._producer.send(self._topic, **kwargs).add_callback(self._onSendSucess).add_errback(self._onSendFailed)
            print("发送消息:", value)
            # 注册回调也可以这样写，上面的写法就是为了简化
            # future.add_callback(self._onSendSucess)
            # future.add_errback(self._onSendFailed)
        except KafkaTimeoutError as err:
            print(err)
        except Exception as err:
            print(err)
 
    def closeConnection(self, timeout=None):
        # 关闭生产者，可以指定超时时间，也就是等待关闭成功最多等待多久。
        self._producer.close(timeout=timeout)
 
    def sendNow(self, timeout=None):
        # 调用flush()函数可以放所有在缓冲区的消息记录立即发送，即使ligner_ms值大于0.
        # 这时候后台发送消息线程就会开始立即发送消息并且阻塞在这里，等待消息发送成功，当然是否阻塞取决于acks的值。
        # 如果不调用flush函数，那么什么时候发送消息取决于ligner_ms或者batch任意一个条件满足就会发送。
        try:
            self._producer.flush(timeout=timeout)
        except KafkaTimeoutError as err:
            print(err)
        except Exception as err:
            print(err)
 
 
def parse(res):
    result = res.result()  # !取到res结果 【回调函数】带参数需要这样
    print(result)

def main_multi():
    p = Producer(KafkaServerList=["172.20.25.34:9092"], ClientId="Procucer02", Topic="AsyncEvent")
    closePrice = random.randint(1, 500)
    msg = {
        "Publisher": "Procucer02",
        "股票代码": 60000 + i,
        "昨日收盘价": closePrice,
        "今日开盘价": 0,
        "今日收盘价": 0,
    }
    p.sendMessage(value=msg)
    # p.sendNow()
    p.closeConnection()
    return msg

def main():
    p = Producer(KafkaServerList=["172.20.25.34:9092"], ClientId="Procucer03", Topic="AsyncEvent")
    for i in range(10):
        time.sleep(1)
        closePrice = random.randint(1, 500)
        msg = {
            "Publisher": "Procucer03",
            "股票代码": 60000 + i,
            "昨日收盘价": closePrice,
            "今日开盘价": 0,
            "今日收盘价": 0,
        }
        p.sendMessage(value=msg)
    # p.sendNow()
    p.closeConnection()
    return 

#多进程
if __name__ == "__main__":
    thread_num = 10
    try:
        startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(startTime)
        pool = ThreadPoolExecutor(max_workers=thread_num,thread_name_prefix='send_kafka')
        for i in range(0,thread_num):
            feature = pool.submit(main_multi).add_done_callback(parse)

        pool.shutdown(wait=True)
        # main()
        endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(endTime)
    finally:
        sys.exit()
# #单进程
# if __name__ == "__main__":
#     try:
#         startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#         print(startTime)
#         main()
#         endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#         print(endTime)
#     finally:
#         sys.exit()