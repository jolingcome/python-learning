# flask日志使用标准的pythonlogging。所有与flask相关的消息都用app.logger来记录，
# 同样的，这个日志记录器也可用于你自己的日志记录。

# 默认情况下，flask会自动添加一个StreamHandler到app.logger。
# 在请求过程中，它会写到由WSGI服务器指定的，
# 保存在environ['wsgi.errors']变量中的日志流(通常是sys.stderr)中。
# 在请求之外，则会记录到sys.stderr。

from flask import Flask,jsonify
import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "info.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "errors.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8",
            },
            "debug_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "debug.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "my_module": {"level": "ERROR", "handlers": ["console"], "propagate": "no"}
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["error_file_handler", "debug_file_handler"],
        },
    }
)

app=Flask(__name__)

@app.route('/login',methods=['GET'])
def login():
    app.logger.debug(f"login success.")
    return jsonify(
        {
            "code":200
        }
    )

if __name__=="__main__":
    app.run(debug=True,port=5001)