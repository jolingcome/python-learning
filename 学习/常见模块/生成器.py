# https://www.zhihu.com/question/19866531
#生成器的使用场景
# (1)节省内存
# (2)流式处理数据
# (3)无限的数据

#为什么要使用生成器？而不是直接使用函数
# 1、通过列表生成式可以直接创建一个列表,但是受到内存的限制,可能创建一个很大的空间,但是实际情况中用不到那么多(在C语言中所谓的堆区,没释放)
#
# 2、生成器(generator)的定义就是根据列表元素可以动态的分配内存空间
#
# 3、在实际开发过程中,如果我们要读取一个十几G大的文件,如果是直接使用文件打开的方式,其实底层的全部加载在内存中,这样造成计算机内存消耗,造成计算机卡死的局面,如果我们使用生成器,把大文件做成文档碎片的方式,每次从中间读取一点出来,然后再释放内存,这样就不会对计算机造成卡死的局面。


# 如：for i in range(10000000):
        # result=[]
        # result.append(i)
#使用生成器或者迭代器相当于只保存当前的结果，之前的数据丢掉。next相当于指针，next处返回生成器的结果
# 2. 生成器返回结果前加list()输出结果，

# 实现generator的两种方式
#（1）把一个列表生成式的[]改成()，就创建了一个generator
from timeit import timeit

lis =[x*x for x in range(10)]  #生成列表
print(lis)
generator_ex=(x*x for x in range(10)) #生成生成器
for i in generator_ex:
    print(i)
print(generator_ex)
# print(next(generator_ex)) #可以用next一个个取生成器中x的值
print(list(generator_ex))

#(2)在函数中使用yield关键字，函数就变成了一个generator。将普通函数的return改为yield就是一个生成器函数

def positive(limit):
    n=1
    while n<=limit:
        yield n  #生成器，这里暂停，执行n的值，返回到此，再执行下一步
        n+=1
for n in positive(5):
    print(n)

#（3） yield from 关键字
# yield from 后面接一个 可迭代对象 ，等价于用 for in 去单独 yield。
list1=[1,2,3,4]
list2=['a','b','c','d']

def my_gen_1(): #用yield from和下面的 for n in list1:yield n是一样的效果，都是遍历list
    yield from list1
    yield from list2

def my_gen_2():
    for n in list1:
        yield n
    for n in list2:
        yield n
print('my_gen_1 循环结果：', [x for x in my_gen_1()])
print('my_gen_2 循环结果：', [x for x in my_gen_2()])




