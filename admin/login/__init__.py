# -*- coding:utf-8 -*-
# @Time  :2019-12-16 14:02:26
# @Author: 程继瑞
# @File  : __init__.py.py

from flask import Blueprint
# 创建巡查隐患蓝图
login = Blueprint('login', __name__, url_prefix='/login')
from pl_web.admin.login.controller import login_controller

