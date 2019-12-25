# -*- coding:utf-8 -*-
# @Time  : 2019-11-26 17:00:07
# @Author: 程继瑞
# @Description 烟感设备服务
# @File  : WeichuanSmokeService
# @from : flask-sqlacodegen

from apply.smoke.model.SmokeModel import SmokeModel,db,app
from apply.ModelCommon import BaseModel
import time
db.init_app(app)

class SmokeService():

    # 删除
    def del_smoke(self, device_id):
        smoke = SmokeModel.query.get(device_id)
        result = True
        try:
            db.session.delete(smoke)
            db.session.commit()
        except Exception as errors:
            print(errors)
            result = False
        finally:
            return result

    # 查询单条 根据devid 获取当条数据
    def device_get_id(self, device_id):
        data = SmokeModel.query.filter_by(device_id=device_id).first()
        if data:
            return data
        else:
            return None

    # 查询所有设备
    def get_smoke_list(self):
        data = SmokeModel.query.all()
        data = BaseModel().ModelToTuple(SmokeModel, data)
        return data

    # 添加设备
    def add_smoke_device(self, data):
        result = True
        data['id'] = str(BaseModel().create_uuid())
        created_time = int(time.time())
        smoke = SmokeModel(
            id=data.get('id'),
            device_id=data.get('device_id'),
            category_id=data.get('category_id'),
            name=data.get('name'),
            address=data.get('address'),
            voltage =data.get('voltage'),
            gps=data.get('gps'),
            temperature=data.get('temperature'),
            state=data.get('state'),
            created_at=created_time,
            updated_at=created_time,
        )
        try:
            db.session.add(smoke)
            db.session.commit()
        except Exception as errors:
            print(errors)
            result = False
        finally:
            return result

    # 修改设备
    def update_smoke_device(self,smoke, data):
        result = True
        smoke.name = data.get('name')
        smoke.category_id = data.get('category_id')
        smoke.address = data.get('address')
        smoke.updated_at = int(time.time())
        try:
            db.session.commit()
        except Exception as errors:
            print(errors)
            result = False
        finally:
            return result

    # 修改状态
    def update_smoke_device_state(self,smoke, data):
        result = True
        smoke.state = data.get('state')
        smoke.updated_at = int(time.time())
        try:
            db.session.commit()
        except Exception as errors:
            print(errors)
            result = False
        finally:
            return result