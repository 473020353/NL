# -*- coding:utf-8 -*-
# @Time  : 2019-12-16 10:59:08
# @Author: 程继瑞
# @Description 登录模块
# @File  : LoginController
# @Remark  :ReturnParam:返回参数,info可以为元组或者string,status默认'success',可以为空;
# @Remark  :ReceiveData:接受参数,返回一个元组

from pl_web.admin.main import main
from pl_web.RestCommon import ReceiveData,ParameterValidate,ErrorInfo,ReturnParam
from flask import render_template

# 后台首页
@main.route('/index', methods=['GET'])
def index():
    return render_template('base/base.html')
