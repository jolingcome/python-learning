#docker-py的使用
#官方文档：【https://docker-py.readthedocs.io/en/stable/images.html】
#pip install docker-py

#实例化一个dockerapi调用者实例
#初始化实例的过程中用到了参数base_url，它可以指出一个socket文件或者响应的dockerTCP连接如tcp://127.0.0.1:2375这样子。
# 除此之外，还有version参数可以指出docker的版本，timeout参数指出连接超时的时间，
# tls参数可以置True或False来指出当前连接是否需要用到SSL证书，另外也可以传递一个docker.tls.TLSConfig类的实例来实现指定的TLS配置。

import docker
#base_url='tcp://10.198.22.43:2375'
base_url='unix://var/run/docker.sock'
docker.DockerClient(base_url)
client1=docker.from_env()
print(client1.containers.list())

