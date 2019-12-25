# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pl_web.PlatfromConfig import apply_config_dict
from pl_web.admin.login.controller.login_controller import login
from pl_web.admin.main.controller.main_controller import main
from pl_web.admin.device_info.controller.device_controller import device

db = SQLAlchemy()
app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(main)
app.register_blueprint(device)

# 工厂方法,根据不同的参数,创建不同环境下的app对象
def create_app(config_name):
    # 根据传入的config_name获取到对应的配置类
    config = apply_config_dict[config_name]
    # 日志方法调用
    # log_file(config.LEVEL)
    # 加载配置类的中配置信息
    app.config.from_object(config)
    # 初始化db中的app
    db.init_app(app)
    # 注册蓝图对象
    return app


# 日志文件,作用:用来记录程序的运行过程,比如:调试信息,接口访问信息,异常信息
def log_file(level):
    # 设置日志的记录等级,设置日志等级: 常见等级有:DEBUG < INFO < WARING < ERROR < FATAL(CRITICAL)
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件编号
    file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

if __name__ == '__main__':
    app = create_app('develop')
    app.run(host='0.0.0.0', port=5555, debug=True)
