# -*- coding:utf-8 -*-
# @Time  : 2019-12-18 15:55:49
# @Author: 程继瑞
# @Description 设备模块
# @File  : DeviceModel(VT)

from pl_web.ModelCommon import BaseModel
from sqlalchemy import Column, String

db = BaseModel().create_db(__name__)[0]
app = BaseModel().create_db(__name__)[1]

class DeviceModel(db.Model):
    """设备 vt"""
    __tablename__ = 'vt_basic_info'
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    devid = Column(String(64), nullable=False, index=True)
    devui = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    gps = Column(String(255), nullable=False)
    bindvn = Column(String(24), index=True)
    bindva = Column(String(24), index=True)

    #  model对象转为字典
    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "devid": self.devid,
            "devui": self.devui,
            "type": self.type,
            "gps": self.gps,
            "bindvn": self.bindvn,
            "bindva": self.bindva
        }
        return data