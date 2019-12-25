# -*- coding:utf-8 -*-
# @Time  : 2019-12-18 16:13:57
# @Author: 程继瑞
# @Description vt设备服务
# @File  : device_service
# @from : flask-sqlacodegen
from pl_web.admin.device_info.model.device_model import DeviceModel,db,app
from pl_web.ModelCommon import BaseModel
import time
from  sqlalchemy import or_
db.init_app(app)

class DeviceService():

    def count_info(self):
        data = DeviceModel.query.all()
        data = BaseModel().ModelToTuple(DeviceModel, data)
        return  data

    # 查询所有设备数据
    def get_device_list(self,page,rows,devid,devui):
        data = DeviceModel.query.filter(DeviceModel.devid.like("%" + devid + "%") if devid is not None else "",DeviceModel.devui.like("%" + devui + "%") if devui is not None else "").paginate(page,rows).items
        data = BaseModel().ModelToTuple(DeviceModel, data)
        return data

    # 条件查询
    def device_exist(self,devui):
        # data = DeviceModel.query.filter(or_(DeviceModel.devid == devid,DeviceModel.devui == devui)).items
        # data = DeviceModel.query.filter_by(devid == '1').first

        data = DeviceModel.query.filter_by(devui=devui).first()
        if data:
            return True
        else:
            return False

        data = BaseModel().ModelToTuple(DeviceModel, data)
        return data

    # 添加
    def add_device(self, data):
        result = True
        data['id'] = str(BaseModel().create_uuid())
        device = DeviceModel(
            id=data.get('id'),
            name=data.get('name'),
            devid=data.get('devid'),
            devui=data.get('devui'),
            gps=data.get('gps'),
            type=data.get('type'),
            bindva=data.get('bindva'),
            bindvn=data.get('bindvn'),
        )
        try:
            db.session.add(device)
            db.session.commit()
        except Exception as errors:
            print(errors)
            result = False
        finally:
            return result