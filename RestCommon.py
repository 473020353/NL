# -*- coding:utf-8 -*-
# @Time  : 2019-11-25 17:37:22
# @Author: 程继瑞
# @Description Rest通信(获取token,token验证,post/get参数解析,返回参数格式定义)
# @File  : RestCommon.py

from flask import jsonify, request
import requests
from pl_web.RestUrlConfig import RestUrlConfig


class APIException(Exception):
    def __init__(self, status, info):
        Exception.__init__(self)
        self.raw_status = status
        self.info = info

    def to_dict(self):
        result = {
            "status": self.raw_status,
            "info": self.info,
        }
        return result


# POST/GET 参数解析认证 + Token 验证
def ReceiveData(debug=True, valid_token=True):
    ''' from requests get json data
        debug: if debug=True, will print requests infos
    '''
    data = None
    if request.method == 'POST':
        data = request.get_json(force=True, silent=True)
    if request.method == 'GET':
        data = {}
        for k, v in request.values.items():
            data[k] = v
    if not data:
        raise APIException('err', ErrorInfo.get_data_error)
    if valid_token:
        token = data.get('token', 'is_empty_token')
        content = Token.restore_token(token)
        if content is False:
            raise APIException('err', ErrorInfo.token_error)
    if debug:
        print("Request:<{}:{}> Data:{}".format(request.method, request.url, data))
    return data

# 参数返回
def ReturnParam(info='sucess', status='ok', debug=True, **kwargs):
    print(info)
    msg = {}
    msg["status"] = status
    msg["info"] = info
    if kwargs:
        for key in kwargs:
            msg[key] = kwargs[key]
    if debug:
        resp = "Response:<{}:{}> Data:{}".format(request.method, request.url, msg)
    return jsonify(msg)

# 报错信息
class ErrorInfo:
    error = 'err'
    error_404 = "not find path"
    error_405 = "http method err"
    error_500 = "internal err"
    get_data_error = "data format err / get data fail"
    token_error = "token verfiy err"
    db_error = "add to db err"
    parameter_lost = "parameter lost"
    device_exist = "devid alreay exist"
    device_error = "devid  vaid err, pl"
    device_lost = "devid is not exists"

# platform Token REST URL 以及 返回消息的参数
class token_config:
    url_pre = "http://rest.guyuaninfo.com:8000/pl/token/"
    token = 'token'
    status = 'status'
    ok_status = 'ok'
    content = 'content'
    exptime = 'expiry_time'

# platform 请求TOKEN 验证类
class Token():

    @staticmethod
    def verify_token(token):
        url = token_config.url_pre + "verify"
        valid = False
        try:
            status = requests.post(url, json={token_config.token: token}, timeout=10).json().get(token_config.status)
            if status == token_config.ok_status:
                valid = True
        finally:
            return valid

    @staticmethod
    def get_token(content=None, exp_time=60 * 60 * 2):
        url = token_config.url_pre + "get"
        token = None
        data = {}
        try:
            data[token_config.exptime] = exp_time
            if content:
                data[token_config.content] = content
            result = requests.post(url, json=data).json()
            if result.get(token_config.status) == token_config.ok_status:
                token = result.get(token_config.token)
        except Exception as e:
            print('get token err:', e)
        finally:
            return token

    @staticmethod
    def get_sys_token(content=None):
        url = token_config.url_pre + "get-sys-token"
        token = None
        data = {}
        try:
            if content:
                data[token_config.content] = content
            result = requests.post(url, json=data).json()
            if result.get(token_config.status) == token_config.ok_status:
                token = result.get(token_config.token)
        except Exception as e:
            print('get sys token err:', e)
        finally:
            return token

    @staticmethod
    def restore_token(token):
        url = token_config.url_pre + "restore"
        content = False
        try:
            content = requests.post(url, json={token_config.token: token}, timeout=10).json()
            if content.get(token_config.status) == token_config.ok_status:
                content = content.get('content') or 'is_empty_token'
            else:
                content = False
        finally:
            return content

# 参数验证
class ParameterValidate:

    # 参数为空判断
    def is_empty(key_list: list) -> bool:
        if not isinstance(key_list, list):
            raise TypeError('require list')
        if not all(key_list):
            return True
        return False

    # 参数Token验证
    def verify_code(reqid: str, code: str):
        res = requests.post(RestUrlConfig.url_code_verify, json={
            'code': code,
            'reqid': reqid,
            'token': Token.get_token()
        }, timeout=10).json()
        print(res)
        if res.get('status') == 'ok':
            return True
        return False

    def device_bind(vaid, devid):
        result = requests.post(RestUrlConfig.url_bind,
                               json={'devid': devid, 'vaid': vaid, 'projectid': RestUrlConfig.projectid,
                                     'token': Token.get_sys_token()}).json()
        if result.get('status') == 'ok':
            return True
        return False

    def device_unbind(vaid, devid):
        result = requests.post(RestUrlConfig.url_unbind, json={'devid': devid, 'vaid': vaid, 'projectid': RestUrlConfig.projectid,
                                                     'token': Token.get_sys_token()}).json()
        if result.get('status') == 'ok':
            return True
        return False

