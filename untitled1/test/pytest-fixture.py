import pytest

# # 调用方式一
# @pytest.fixture
# def login():
#     print("输入账号，密码先登录")
#
# def test_s1(login):
#     print("用例 1：登录之后其它动作 111")
#
# def test_s2():
#     print("用例 2：不需要登录，操作 222")
#
# #调用方式二
# @pytest.fixture
# def login2():
#     print("please输入账号，密码先登录")
#
# @pytest.mark.usefixtures("login2","login")
# def test_s11():
#     print("用例 11：登录之后其它动作 111")
#
# # 调用方式三
# @pytest.fixture(autouse=True)
# def login3():
#     print("====auto===")
#
# # 不是test开头，加了装饰器也不会执行fixture
# @pytest.mark.usefixtures("login2")
# def loginss():
#     print(123)
#
#
# order = []
#
# @pytest.fixture(scope="session")
# def s1():
#     order.append("s1")
#
#
# @pytest.fixture(scope="module")
# def m1():
#     order.append("m1")
#
#
# @pytest.fixture
# def f1(f3, a1):
#     # 先实例化f3, 再实例化a1, 最后实例化f1
#     order.append("f1")
#     assert f3 == 123
#
#
# @pytest.fixture
# def f3():
#     order.append("f3")
#     a = 123
#     yield a
#
#
# @pytest.fixture
# def a1():
#     order.append("a1")
#
#
# @pytest.fixture
# def f2():
#     order.append("f2")
#
#
# def test_order(f1, m1, f2, s1):
#     # m1、s1在f1后，但因为scope范围大，所以会优先实例化
#     assert order == ["s1", "m1", "f3", "a1", "f1", "f2"]

@pytest.fixture()
def logins(request):
    param = request.param
    print(f"账号是：{param['username']}，密码是：{param['pwd']}")
    return param


data = [
    {"username": "name1", "pwd": "pwd1"},
    {"username": "name2", "pwd": "pwd2"},
]


@pytest.mark.parametrize("logins", data, indirect=True)
def test_name_pwd(logins):
    print(f"账号是：{logins['username']}，密码是：{logins['pwd']}")