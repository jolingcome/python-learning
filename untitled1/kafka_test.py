#连接kafka
# https://pypi.org/project/kafka-python/
#https://zhuanlan.zhihu.com/p/279784873
#https://www.cnblogs.com/luoyc/p/12097974.html 也可以用pykafka包

import ssl
import sys
import os
from kafka import KafkaProducer,KafkaConsumer,KafkaClient


# Cluster_name="sfe-int-183-v1.0"
# Zookeeper_Host="sfe-int-183"
# Zookeeper_Port=30181
# SASL="SASL Plaintext"
# Bootstrap_servers="sfe-int-183:30094"
# SASL_Mechanism="PLAIN"
# username="admin"
# password="admin"

#获取所有的topic
def kafka_topciList(ip):
    consumer=KafkaConsumer(
            bootstrap_servers=['%s:30094'%ip],
            sasl_plain_username="admin",  # 配置login
            sasl_plain_password="admin",
            sasl_mechanism="PLAIN",
            security_protocol='SASL_PLAINTEXT')
    for i in consumer.topics():
        print(i)
print(kafka_topciList("10.151.5.183"))#查询toplist

# from pykafka import KafkaClient
# client=KafkaClient(hosts="10.151.5.183:30094")
# print(client.topics)

