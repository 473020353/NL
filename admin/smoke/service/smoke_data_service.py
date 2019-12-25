# -*- coding:utf-8 -*-
# @Time  : 2019-12-2 11:55:44
# @Author: 程继瑞
# @Description 烟感设备数据服务
# @File  : WeichuanDataSmokeService
# @from : flask-sqlacodegen

from apply.smoke.model.smoke_data_model import SmokeDataModel,db,app
from apply.ModelCommon import BaseModel
import time
db.init_app(app)

class SmokeDataService():

    # 删除
    def del_smoke_data(self, device_id):
        smoke = SmokeDataModel.query.get(device_id)
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
        data = SmokeDataModel.query.filter_by(device_id=device_id).first()
        if data:
            return data
        else:
            return None

    # 查询所有设备数据
    def get_smoke_list(self):
        data = SmokeDataModel.query.all()
        data = BaseModel().ModelToTuple(SmokeDataModel, data)
        return data

    #  添加设备数据
    def add_smoke_device_data(self, data):
        result = True
        data['id'] = str(BaseModel().create_uuid())
        created_time = int(time.time())
        smoke = SmokeDataModel(
            id=data.get('id'),
            device_id=data.get('device_id'),
            voltage =data.get('voltage'),
            temperature=data.get('temperature'),
            state=data.get('state'),
            created_at=created_time,
            time=time
        )
        try:
            db.session.add(smoke)
            db.session.commit()
        except Exception as errors:
            print(errors)
            result = False
        finally:
            return result

