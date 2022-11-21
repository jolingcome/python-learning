# Faker是一个专门用来生成模拟数据的一个python库，利用它可以虚拟出各式各样的数据，用于调试、测试等。
# 利用的Faker的provider机制，我们甚至还可以自定义自己的模拟数据方法，实现Faker库中没有的功能。
# https://faker.readthedocs.io/en/master/index.html#
from faker import Faker

fake1=Faker() #实例化
print(fake1.name())
print(fake1.first_name())
print(fake1.email())
print(fake1.url())