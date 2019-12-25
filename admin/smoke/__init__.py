# -*- coding:utf-8 -*-
# @Time  : 2019-11-20 10:24
# @Author: 程继瑞
# @File  : __init__.py.py


from flask import Blueprint
# 创建巡查隐患蓝图
smoke = Blueprint('smoke', __name__, url_prefix='/device/smoke')
from apply.smoke.controller import smoke_controller

