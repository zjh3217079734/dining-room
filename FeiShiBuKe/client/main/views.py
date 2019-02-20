# 处理与客户相关的路由和视图
from . import main
from flask import Flask, render_template, request, session, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
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

@main.route('/')
def index_views():
    if 'username' in request.cookies:
        username = request.cookies['username']
    return render_template('index.html', params=locals())


@main.route("/<name>")
def html(name=None):
    return render_template(name, params=locals())
# -------------------------------------------

# ----------------------------------------
# localhost:5000/cart-page.html
# 购物车后台部分


# @main.route('/cart-page')
# def cart_page_viwes():
#     # # 1. 获取当前订单号
#     # order_id = request.args['order_id']
#     # # 2. 根据订单号,查询出订单下菜品详情
#     # goods = db.session.query(order_details)
#     pass

# -----------------------------------------------------------
# 应巧
@main.route('/')
def index_views():
    if 'username' in request.cookies:
        username = request.cookies['username']
    return render_template('index.html', params=locals())


@main.route('/login', methods=['POST', 'GET'])
def login_views():
    if request.method == 'GET':
        url = request.headers.get('Referer', '/')
        session['url'] = url
        # return render_template('login-register.html')
        if 'username' in session:
            return redirect(url)
        else:
            if 'username' in request.cookies:
                username = request.cookies['username']
                users = user_info.query.all()
                if username in users:
                    session['username'] = username
                    return redirect(url)
                else:
                    resp = make_response(
                        render_template(
                            'login-register.html',
                            params={}))
                    resp.delete_cookie('username')
                    return resp
            else:
                return render_template('login-register.html', params={})
    else:
        username = request.form['username']
        password = request.form['password']
        user = user_info.query.filter_by(
            user_name=username, password=password).first()
        if user:
            session['id'] = user.id
            session['username'] = username
            url = session['url']
            resp = redirect(url)
            if 'isSaved' in request.form:
                resp.set_cookie('username', username, 60 * 60 * 24 * 365 * 10)
            return resp
        else:
            errMsg = "用户名或密码不正确"
            return render_template('login-register.html', params=locals())


@main.route('/register', methods=['GET', 'POST'])
def register_views():
    if request.method == 'GET':
        return render_template('login-register.html', params={})
    else:
        username = request.form['uname']
        password = request.form['upwd']
        phone = request.form['uphone']

        user = user_info()
        user.user_name = username
        user.password = password
        user.phone = phone
        try:
            db.session.add(user)
            db.session.commit()
            return render_template('index.html', params=locals())
        except Exception as ex:
            print(ex)
            return "注册失败，请联系管理员！"


@main.route('/logout')
def logout_views():
    url = request.headers.get('Referer', '/')
    resp = redirect(url)
    if 'username' in request.cookies:
        resp.delete_cookie('username')
    return resp


@main.route('/register/checkuname')
def checkuname():
    uname = request.args['uname']
    users = user_info.query.filter_by(user_name=uname).all()
    if users:
        return "1"
    else:
        return "0"

# -----------------------------------------------------------
