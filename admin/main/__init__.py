# -*- coding:utf-8 -*-
# @Time  :2019-12-16 14:02:26
# @Author: 程继瑞
# @File  : __init__.py.py

from flask import Blueprint
# 创建巡查隐患蓝图
main = Blueprint('main', __name__, url_prefix='/main')
from pl_web.admin.main.controller import main_controller

