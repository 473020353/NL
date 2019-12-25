# -*- coding:utf-8 -*-
# @Time  : 2019-11-25 14:58:42
# @Author: 程继瑞
# @Description 烟感设备模块
# @File  : SmokeModel

from apply.ModelCommon import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import FetchedValue

db = BaseModel().create_db(__name__)[0]
app = BaseModel().create_db(__name__)[1]

class SmokeModel(db.Model):
    """烟感设备 SmokeModel"""

    id = Column(String(255, 'utf8_bin'), primary_key=True)
    category_id = Column(String(255, 'utf8_bin'), nullable=False)
    name = Column(String(255, 'utf8_bin'), nullable=False)
    device_id = Column(String(64, 'utf8_bin'), nullable=False, index=True)
    address = Column(String(255, 'utf8_bin'))
    gps = Column(String(255, 'utf8_bin'))
    voltage = Column(String(255, 'utf8_bin'))
    temperature = Column(String(255, 'utf8_bin'))
    state = Column(String(10, 'utf8_bin'), server_default=FetchedValue())
    created_at = Column(Integer)
    updated_at = Column(Integer)

    #  model对象转为字典
    def to_dict(self):
        data = {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "person": self.person,
            "device_id": self.device_id,
            "address": self.address,
            "gps": self.gps,
            "voltage": self.voltage,
            "temperature": self.temperature,
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return data