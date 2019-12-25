# -*- coding:utf-8 -*-
# @Time  : 2019-11-25 14:58:42
# @Author: 程继瑞
# @Description 烟感设备模块
# @File  : SmokeController
# @Remark  :ReturnParam:返回参数,info可以为元组或者string,status默认'success',可以为空;
# @Remark  :ReceiveData:接受参数,返回一个元组

from apply.smoke.service.smoke_service import SmokeService
from apply.smoke import smoke
from apply.RestCommon import ReceiveData,ParameterValidate,ErrorInfo,ReturnParam

# 获取所有
@smoke.route('/smoke_device_list', methods=['GET', 'POST'])
def get_smoke_device_list():
    data = SmokeService().get_smoke_list()
    return ReturnParam(info=data)

# 获取单条
@smoke.route('/smoke_device_one_message', methods=['POST'])
def devid_get_id():
    data = ReceiveData(True,False)
    device_id = data.get('devid')
    result = SmokeService().device_get_id(device_id)
    return ReturnParam(info=result)

# 删除
@smoke.route('/smoke_device_delete', methods=['POST'])
def smoke_device_delete():
    data = ReceiveData()
    # 参数device_id 缺失
    # if ParameterValidate.is_empty([data.get('device_id')]):
    #     return ReturnParam(info=ErrorInfo.get_data_error,status=ErrorInfo.error)
    # 解绑
    # if not ParameterValidate.device_unbind(vaid=data.get('vaid'),devid=data.get('devid')):
    #     return ReturnParam(info=ErrorInfo.device_error,status=ErrorInfo.error)
    smoke = SmokeService().device_get_id(data.get('device_id'))
    if not smoke:
        return ReturnParam(info=ErrorInfo.device_lost,status=ErrorInfo.error)
    if SmokeService().del_smoke(smoke.id):
        return ReturnParam(info='delete device success',status='ok')
    return ReturnParam(info='delete device fail ',status='err')

# 添加设备
@smoke.route('/smoke_device_add', methods=['POST'])
def smoke_device_add():
    data = ReceiveData()
    device_id = data.get("device_id")
    category_id = data.get("category_id")
    name = data.get("name")
    # 关键参数是否为空
    if ParameterValidate.is_empty([name,category_id,device_id]):
        return ReturnParam(info=ErrorInfo.parameter_lost,status=ErrorInfo.error)
    # PL绑定关系
    # if not ParameterValidate.device_bind(vaid=vaid,devid=devid):
    #     return ReturnParam(info=ErrorInfo.device_error,status=ErrorInfo.error)
    # 是否已经存在的设备
    if SmokeService().device_get_id(device_id):
        return ReturnParam(info=ErrorInfo.device_exist, status=ErrorInfo.error)
    # 添加设备
    if SmokeService().add_smoke_device(data):
        return ReturnParam(info='smoke device add success')
    return ReturnParam(info="smoke device add fail")

# 修改
@smoke.route('/smoke_device_edit', methods=['POST'])
def smoke_device_edit():
    data = ReceiveData()
    device_id = data.get("device_id")
    category_id = data.get("category_id")
    name = data.get("name","")
    # 关键参数是否为空
    if ParameterValidate.is_empty([name, category_id, device_id]):
        return ReturnParam(info=ErrorInfo.parameter_lost, status=ErrorInfo.error)
    # 查询参数是否存在
    smoke = SmokeService().device_get_id(device_id)
    if not smoke:
        return ReturnParam(info=ErrorInfo.device_lost, status=ErrorInfo.error)
    # 进行参数修改
    if SmokeService().update_smoke_device(smoke,data):
        return ReturnParam(info="update success")
    return ReturnParam(info="updates fail")



