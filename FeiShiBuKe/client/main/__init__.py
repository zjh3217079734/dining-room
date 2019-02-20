# main:处理与客户相关的 业务逻辑(主业务)
# 将自己添加到蓝图中
from flask import Blueprint
main = Blueprint("main", __name__)
from . import views
