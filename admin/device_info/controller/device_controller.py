# -*- coding:utf-8 -*-
# @Time  : 2019-12-18 09:30:26
# @Author: 程继瑞
# @Description 设备模块
# @File  : DeviceController
# @Remark  :ReturnParam:返回参数,info可以为元组或者string,status默认'success',可以为空;
# @Remark  :ReceiveData:接受参数,返回一个元组
from pl_web.admin.device_info import device
from pl_web.RestCommon import ReceiveData,ParameterValidate,ErrorInfo,ReturnParam
from flask import render_template, send_file,request
from pl_web.admin.device_info.service.device_service import DeviceService
# 加载页面
@device.route('/index', methods=['GET'])
def index():
    return render_template('device/index.html')

@device.route('/device_info',methods=['POST'])
def device_info():
    devid = request.form.get('devid') if request.form.get('devid') else ''
    devui = request.form.get('devui') if request.form.get('devui') else ''    
    page = int (request.form.get('page')) if request.form.get('page') else 1
    rows = int(request.form.get('rows')) if request.form.get('rows') else 20
    device_info = DeviceService().get_device_list(page,rows,devid,devui)
    number = len(DeviceService().count_info())
    data = {"total": number,
            "rows": device_info
            }
    return data

@device.route('/device_add',methods=['POST'])
def device_add():
    data = request.values.to_dict()
    if data is None:
        return ReturnParam(info='参数不能为空', status='error')
    if DeviceService().device_exist(data.get('devui')):
        return ReturnParam('已经存在的Devui', 'error')
    if DeviceService().add_device(data):
        return ReturnParam('添加成功', 'success')
    else:
        return ReturnParam('失败', 'error')