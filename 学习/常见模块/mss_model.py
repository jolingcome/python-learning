#https://xugaoxiang.com/2022/09/22/python-module-37-mss/
#mss 是个截图包，默认是全屏
import mss

# def fun_callback(filename):
#     print(filename)
#
# #1.截取全屏窗口
# with mss.mss() as sct:
#     #通过参数output指定保存的文件名
#     sct.shot(output='output.png',callback=fun_callback) #callback,方便我们使用回调
#
# #2.截取部分窗口
# with mss.mss() as sct_1:
#     # 设置一个区域，top为距离屏幕左上角的垂直方向上的距离，left是水平方向的距离，后面2个分别是宽和高
#     monitor={"top":50,"left":50,"width":600,"height":400}
#     image_sct=sct_1.grab(monitor)
#     #转换成png保存起来
#     mss.tools.to_png(image_sct.rgb,image_sct.size,output="output1.png")

# #3.将mss的图片格式转换成PIL
# from PIL import Image
# with mss.mss() as sct_2:
#     # 设置一个区域，top为距离屏幕左上角的垂直方向上的距离，left是水平方向的距离，后面2个分别是宽和高
#     monitor = {"top": 50, "left": 50, "width": 600, "height": 400}
#     image_sct=sct_2.grab(monitor)
#     image_pil=Image.frombytes("RGB",image_sct.size,image_sct.bgra,'raw','BGRX')
#     image_pil.save('out_pil.png')

#4. 借助opencv，进行录屏
import cv2
import numpy as np
from PIL import Image

monitor = {"top":50, "left":50, "width": 600, "height": 400}
fourcc=cv2.VideoWriter_fourcc(*'MJPG')
fps=20
video=cv2.VideoWriter('output.avi',fourcc,fps,(600,400))
with mss.mss() as sct_3:
    while True:
        image_sct=sct_3.grab(monitor)
        image_pil=Image.frombytes('RGB',image_sct.size,image_sct.bgra,'raw','BGRX')
        image_cv=np.array(image_pil)
        video.write(image_cv)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
video.release()

#备注：PIL 图片的使用
# PIL.Image.frombytes()根据缓冲区中的像素数据创建图像存储器的副本。以最简单的形式，此函数采用三个参数(模式，大小和解压缩的像素数据)。
# 用法： PIL.Image.frombytes(mode, size, data, decoder_name=’raw’, *args)
# 参数:
# mode-图像模式。请参阅：模式。
# size-图像尺寸。
# data-包含给定模式原始数据的字节缓冲区。
# decoder_name-使用什么解码器。
# args-给定解码器的其他参数。
#
# 返回:Image对象。

