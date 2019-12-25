# -*- coding:utf-8 -*-
# @Time  : 2019-12-2 11:31:09
# @Author: 程继瑞
# @Description 烟感数据模块
# @File  : SmokeDataModel

from apply.ModelCommon import BaseModel
from sqlalchemy import Column, Integer, String

db = BaseModel().create_db(__name__)[0]
app = BaseModel().create_db(__name__)[1]

class SmokeDataModel(db.Model):
    """烟感数据设备 smoke_device_data"""
    __tablename__ = 'smoke_data'
    id = Column(String(200, 'utf8_bin'), primary_key=True)
    device_id = Column(String(255, 'utf8_bin'), index=True)
    voltage = Column(String(255, 'utf8_bin'))
    temperature = Column(String(255, 'utf8_bin'))
    time = Column(String(255, 'utf8_bin'))
    state = Column(String(255, 'utf8_bin'))
    created_at = Column(Integer)

    #  model对象转为字典
    def to_dict(self):
        data = {
            "id": self.id,
            "device_id": self.device_id,
            "voltage": self.voltage,
            "temperature": self.temperature,
            "state": self.state,
            "time": self.time,
            "created_at": self.created_at,
        }
        return data