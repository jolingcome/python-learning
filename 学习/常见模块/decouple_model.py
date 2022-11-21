# 将设置从代码中分离开
# decouple将帮助你解析你的程序配置文件，达到更改你的设置而不用重新部署程序的效果

# decouple完成的事情：
# # 1. 在ini或者.env文件中存储你的参数
# # 2. 定义你的默认值
# # 3. 适当的将你的配置转换成合适的值
# # 4. 你的程序中只需要一个配置模块来进行设置
# Decouple支持两种类型：.ini文件和.env 文件

# pip install python-decouple

from decouple import config
from unipath import Path
from dj_database_url import parse as db_url

BASE_DIR = Path(__file__).parent
DEBUG = config('DEBUG', default=False,cast=bool)
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
        cast=db_url
    )
}

TIME_ZONE = 'America/Sao_Paulo'
USE_L10N = True
USE_TZ = True

# SECRET_KEY = config('SECRET_KEY')
#
# EMAIL_HOST = config('EMAIL_HOST', default='localhost')
# EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

