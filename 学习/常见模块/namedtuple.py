# namedtuple是继承自tuple的子类。namedtuple创建一个和tuple类似的对象，而且对象拥有可访问的属性
# 因为元组的局限性：不能为元组内部的数据进行命名，所以往往我们并不知道一个元组所要表达的意义，
# 所以在这里引入了 collections.namedtuple 这个工厂函数，来构造一个带字段名的元组。
# 具名元组的实例和普通元组消耗的内存一样多，因为字段名都被存在对应的类里面。这个类跟普通的对象
# 实例比起来也要小一些，因为 Python 不会用 __dict__ 来存放这些实例的属性。
# 在映射中可以当键使用，而 namedtuple 不仅可以通过索引来访问，还可以通过属性名称来访问，同时还支持属性值的修改。
from collections import namedtuple

# 定义一个namedtuple类型的Worker，列表中是它的属性
Worker=namedtuple('Worker',['name', 'sex', 'id', 'salary'])
#实例化对象
w1=Worker('alex', 'male', '001', '10000')
# 通过索引获取值
print(w1[0])
# 通过名称获取值
print(w1.salary)

# 通过_make方法来实例化，参数是一个list
w2 = Worker._make(['lily', 'female', '002', '11000'])
print(w2.name)
print(w2.salary)

# 修改对象的属性
print(w2._replace(salary='15000'))

# 通过方法_asdict，可以转换成字典
print(w1._asdict())