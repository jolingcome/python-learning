#docker-py的使用
#官方文档：【https://docker-py.readthedocs.io/en/stable/images.html】
#pip install docker-py

import docker


#实例化一个dockerapi调用者实例
#初始化实例的过程中用到了参数base_url，它可以指出一个socket文件或者响应的dockerTCP连接如tcp://127.0.0.1:2375这样子。
# 除此之外，还有version参数可以指出docker的版本，timeout参数指出连接超时的时间，
# tls参数可以置True或False来指出当前连接是否需要用到SSL证书，另外也可以传递一个docker.tls.TLSConfig类的实例来实现指定的TLS配置。
base_url='tcp://10.198.22.43:2375'
client = docker.client(base_url)
print(client)
# client=docker.DockerClient(base_url)
# for component,version in client.version().iteritems():
#     print(component,version)

# 其他的读取当前docker环境中的一些方法如：
# client.images([name])　　获取镜像信息，name可以是一个镜像的name，name的一部分，name:tag等多种形式，获取到完整的镜像信息。不指定name时返回所有镜像信息
# client.containers([name])　　获取容器信息，name可以是容器的name, id等等，返回
# client.info()　　docker info命令的那些输出
# client.start/stop(name)　　相当于docker start和stop制定容器

# client.login()　　可以传入实名参数username, password, registry等，相当于docker login