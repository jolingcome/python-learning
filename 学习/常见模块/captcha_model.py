# captcha是一个用来生成图片或音频验证的第三方库，验证码技术在 web 应用中非常常见。本篇我们就来看看它的一些常见用法。
# https://xugaoxiang.com/2022/08/24/python-module-36-captcha/
import argparse
from captcha.image import ImageCaptcha  #图片
from captcha.audio import AudioCaptcha #语音

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--text',type=str,default='xugaoxiang',help='text that show in the image')
    opt=parser.parse_args()
    print(opt)

    # 实例化，指定宽度和高度，如果想更换显示的字体，可以使用参数 fonts
    image=ImageCaptcha(width=300,height=100)
    captcha_text=opt.text
    #生成图片
    data = image.generate_image(captcha_text)
    #保存图片
    image.write(captcha_text,'captach.png')

#在terminal中执行：python D:\代码\python\学习\常见模块\captcha_model.py --text keiw 生成keiw的图片
    #接下来，再看语音验证码的实例
    audio=AudioCaptcha()
    captcha_text_autio='1234'
    audio_data=audio.generate(captcha_text_autio)
    audio.write(captcha_text_autio,'out.wav')
    # 不指定语音目录的情况下，默认只能生成数字的，如果要生成字符的，代码就会报错。这时，我们可以创建自己的语音库，利用
    # espeak(文本转语音)和ffmpeg(语音处理)这2个工具便可以实现



