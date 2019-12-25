# -*- coding:utf-8 -*-
# @Time  :2019-12-18 09:29:07
# @Author: 程继瑞
# @File  : __init__.py.py

from flask import Blueprint
# 创建蓝图
device = Blueprint('device', __name__, url_prefix='/device')
from pl_web.admin.device_info.controller import device_controller

