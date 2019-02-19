# 处理与客户相关的路由和视图
from . import main
from flask import Flask, render_template, request, session, redirect
from datetime import datetime
import os
import json
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import *
from .. import db
# -*- coding: utf-8 -*-
import httplib2
from urllib.parse import urlencode  # python3
# from urllib import urlencode #python2


@main.route("/SelectCity")
def SelectCity():
    city = request.args["city"]
    return city


@main.route("/")
@main.route("/<name>")
def html(name=None):
    if name is None or name == "index":
        return render_template("index.html", params=locals())
    return render_template(name, params=locals())
# -------------------------------------------

# ----------------------------------------
# localhost:5000/cart-page.html
# 购物车后台部分


@main.route('/cart-page')
def cart_page_viwes():
    # # 1. 获取当前订单号
    # order_id = request.args['order_id']
    # # 2. 根据订单号,查询出订单下菜品详情
    # goods = db.session.query(order_details)
    pass

# ---------------------------------------
# 应巧


@main.route('/login', methods=['GET', 'POST'])
def login_views():
    if request.method == 'GET':
        return render_template('login-register.html')
    else:
        user_name = request.form['username']
        password = generate_password_hash(request.form['password'])
        print("用户名:%s,密码:%s" % (user_name, password))
        result = check_password_hash(password, '123456')
        if result:
            print('密码为123456')
        else:
            print('密码不是123456')
        return "接收数据成功"


@main.route('/register', methods=['GET', 'POST'])
def register_views():
    if request.method == 'GET':
        return render_template('login-register.html')
    else:
        user_name = request.form['username']
        password = generate_password_hash(request.form['password'])
        phone = request.form['phonenum']
        print("用户名:%s,密码:%s,手机号:%s" % (user_name, password, phone))
        result = check_password_hash(password, '123456')
        if result:
            print('密码为123456')
        else:
            print('密码不是123456')
        return "接收数据成功"
