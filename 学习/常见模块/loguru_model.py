# Python实用模块(十四)logging 已经介绍过了python内置日志模块logging。我们要使用logging，一般来讲，
# 都是需要进行一些基本配置，比如下方的代码片段
# import logging
#
# logging.basicConfig(
#     filename='test.log',
#     level=logging.DEBUG,
#     format='[line:%(lineno)d] - %(funcName)s: %(asctime)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
# )

import sys
from loguru import logger
print(logger.debug("hello loguru")) #不需要像上面的logging那样先配置

# 接下来看看handler、formatter、filter的配置，这几个名词跟logging中是一致的。使用logger.add方法来进行配置
logger.add(sys.stderr,format="{time} {level} {message}",filter="my_model",level="INFO")
print(logger.debug("hello loguru"))

#将日志写入文件中
logger.add("log_{time}.log")
logger.debug("Hello aa")

# 关于rotation部分，使用rotation可让loguru支持按文件大小、时间、保留时长等
logger.add("log.log", rotation="500 MB") # 超过文件大小后拆分
logger.add("log.log", rotation="12:00")  # 每天12点
logger.add("log.log", rotation="1 week") # 保留一周

# 为防止日志挤爆硬盘，可以设置日志的保留时长
logger.add("log.log", retention="7 days")
# 还可以将日志进行压缩
logger.add("log.log", compression="zip")
# 默认情况下，loguru是线程安全的，但是在多进程中并不是。不过，通过参数enqueue可以达到安全的目标
logger.add("log.log", enqueue=True)
