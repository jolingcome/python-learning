#序列化与反序列化的使用场景：
# 1.把对象的字节序列永久地保存到硬盘上，通常存放在一个文件中；
# 2. 在网络上传送对象的字节序列。
# https://www.cnblogs.com/niuyourou/p/12521325.html
# http://t.zoukankan.com/wj-1314-p-8206840.html 序列化详解

# 面向对象的一大特性便是封装，我们将模型的属性和方法封装到一个类中，非静态属性在对象实例化时被赋予具体的值。
# 可以这样理解，对象是 JAVA 层面用于描述一个实体的数据结构，与 XML，JSON无异。在很多场景下，我们需要对其进行保存或传输，在相同或不同的 JVM 之间传递。
# 对象本身就是用于描述一个实体的数据的封装，序列化是将能够完整描述一个对象的特征数据提取出来；
# 反序列化是通过可以完整描述一个对象的特征数据创建一个一摸一样的对象

# 我们看几个典型的使用场景：
#
# 1. Web 服务器中的 Session 会话对象，当有10万用户并发访问，就有可能出现10万个 Session 对象，显然这种情况内存可能是吃不消的。于是 Web 容器就会把一些 Session 先序列化，让他们离开内存空间，序列化到硬盘中，当需要调用时，再把保存在硬盘中的对象还原到内存中。
#
# 2. 当两个进程进行远程通信时，彼此可以发送各种类型的数据，包括文本、图片、音频、视频等， 而这些数据都会以二进制序列的形式在网络上传送。同样的序列化与反序列化则实现了 进程通信间的对象传送，发送方需要把这个Java对象转换为字节序列，才能在网络上传送；接收方则需要把字节序列再恢复为Java对象。
#
# 可以总结为两类用途：对对象进行持久化存储；在不同进程间传递对象。

# 序列化之后，就可以把序列化后的内容写入磁盘，或者通过网络传输到别的机器上（因为硬盘或网络传输时只接受bytes）。
# 反过来，把变量内容从序列化的对象重新读到内存里称之为反序列化，即unpacking。

#
# 我们来看一下如何进行序列化和反序列化。最常使用的序列化方式有三种：
# 　1. XML：把对象序列化成XML格式的文件，然后就可以通过网络传输这个对象或者把它储存进文件或数据库里了。我们也可以从中取出它并且反序列化成原来的对象状态。在JAVA中我们使用 JAXB库。
# 　2. JSON：同样可以把对象序列化成JSON格式从而持久化保存对象。JSON提供了dump()和dumps()方法实现对象的序列化。

#json的序列化和反序列化：
# 对象序列化：dumps:参数是obj，如json.dumps([1,2,3])
# 反序列化：loads:参数是str, 如json.loads('[1,2,3]')
# 需求：
# 创建一个 test.json 的空文件。
# 定义一个 write 函数写入 dict 数据类型的内容到 test.json 文件
# 定义一个 read 函数，将写入到 test.json 文件的内容，反序列化读取出来
import json
import pickle
data={'name': '托尼·史塔克', 'age': 52, 'top': 185}
def read(path):
    with open(path,'rb') as f:
        data =f.read()
    # return json.loads(data)  #可以直接用json反序列化，也可以用pickle.loads()
    return pickle.loads(data)

def write(path,data):
    # 注意：如果直接用json,则json.load参数是str,with open的参数为'w'即：with open(path,'w),
    #pickle 的类型是byte，故witho open 用wb，即：with open(path,'wb')
    with open(path,'wb') as f:
        if isinstance(data,dict):
            # _data=json.dumps(data) #可以用json.dumps序列化，也可以用pickle.dumps()
            _data=pickle.dumps(data)
            print(type(_data))
            f.write(_data)
        else:
            raise TypeError('\'data\' 不是一个字典类型的数据')
    return True

# pickle.dump() 将数据通过特殊的形式转化为只有python语言认识的字符串，并写入文件
# pickle.dumps() 是转化为其它所有语言都认识的字符串
data_1 = {
    'roles':[
        {'role':'monster','type':'pig','life':50},
        {'role':'donkey','type':'dog','life':60},
    ]
}
pk = open('data.pkl','wb')
print(type(pk),pickle.dump(data,pk))

# pickle.load()对文件进行反序列化，得到文件里面保存的数据
data_2 = {
    'roles':[
        {'role':'monster','type':'pig','life':50},
        {'role':'donkey','type':'dog','life':60},
    ]
}

with open('data.pkl','rb') as f:
    result  = pickle.load(f)
    print(result)


if __name__ == '__main__':
    write('test.json', data)
    result = read('test.json')
    print(result)
    result['Sex'] = 'Man'           # 加入 {'Sex': 'Max'} 键值对
    write('test.json', result)      # 将加入的 键值对 写入 test.json 文件
    result_test_json = read('test.json')
    print(result_test_json)
