# PySnooper是一个用于代码调试的一个第三方库，源码地址是 https://github.com/cool-RR/PySnooper，项目简介中只有一句话，
# Never use print for debugging again。相信很多人，特别是新手都是用print来进行代码调试的，
# 那这个项目就能让你摆脱print语句，让你的代码调试更加高效。
import pysnooper

@pysnooper.snoop()
def double(a):
    return 2*a

# 可以看到，for循环执行的每一步及其double函数的返回值。如果没有使用pysnooper的话，那可能就是在for循环中加入print，
# 然后打印出对应的x及double(x)了。
#
# 如果希望将标准输出的内容重定向到文件，可以修改
@pysnooper.snoop('log.txt')
def double(a):
    return 2*a


if __name__ == "__main__":
    for x in range(5):
        double(x)