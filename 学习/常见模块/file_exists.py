#判断文件是否存在

#方法一：
# 通过打开文件的结果来判断，此文件是否存在
try:
    f = open("filename.txt")
except FileNotFoundError:
    # 不存在时做什么事
    pass
else:
    # 存在时做什么事
    pass

#方法二：
# 使用 os.path 模块来判断，比方法一简单好用，文件 io 毕竟是个耗时操作
import os
if os.path.exists('filename.txt'):
    # 文件或目录存在时，做什么事
    pass
else:
    #不存在时做什么事
    pass
if os.path.isfile('filename.txt'):
    #是文件做什么事
    pass
if os.path.isdir("filename"):
    #是目录做什么事
    pass

#方法三:
# 从 python 3.4版本开始，可以使用 pathlib 这个库来处理，无需特别处理各平台的路径(/ 和 \)问题。
# 以上三种方法中，也是推荐使用这种。
from pathlib import Path
the_file=Path("filename.txt")
if the_file.is_file():
    #是文件做什么事
    pass
if the_file.is_dir():
    #是目录做什么事
    pass
if the_file.exists():
    #文件或目录存在时，做什么事
    pass