from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apply.ApplyConfig import *
import uuid

class BaseModel(object):

    # """模型基类，为每个模型补充创建时间与更新时间"""
    # create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    # update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间

    # 查询对象转为元组的方式
    def ModelToTuple(self,model,list):
        return_data = []
        data = tuple(list)
        for i in data:
            return_data.append(model.to_dict(i))
        return tuple(return_data)

    # 创建UUID
    def create_uuid(size=16):
        """ return random uuid(16) ex> '12345554466363'
            size: max is 21, suggess 6-16
        """
        return uuid.uuid4()

    # 初始化model类方法
    def create_db(self,model_name):
        app = Flask(model_name)
        config = apply_config_dict["develop"]
        app.config.from_object(config)
        app.config['SQLALCHEMY_DATABASES_URI'] = ApplyConfig.SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        db = SQLAlchemy(app)
        db.init_app(app)
        return [db,app]

# if __name__ == '__main__':
#     app.run()
