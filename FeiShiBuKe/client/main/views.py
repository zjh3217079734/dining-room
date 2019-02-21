# 处理与客户相关的路由和视图
from . import main
from .. import db
from ..models import *
from flask import Flask, render_template, request, session, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import pymysql
from sqlalchemy import or_, func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# ---------------------------------------------
# localhost:5000/
# 主页部分


# @main.route("/")
# @main.route("/<name>")
# def html(name=None):
#     if name is None:
#         return render_template("index.html")
#     return render_template(name)
# 首页需要判断cookies中是否有登录信息,不然会报错

# -------------------------------------------
# -----------------------------------------------------------
# 应巧
@main.route('/')
def index_views():
    if 'username' in request.cookies:
        username = request.cookies['username']
        return render_template('index.html', params=locals())
    else:
        return render_template('index.html',params=None)


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
                users = User.query.all()
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
        user = User.query.filter_by(
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

        user = User()
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
    users = User.query.filter_by(user_name=uname).all()
    if users:
        return "1"
    else:
        return "0"

# -----------------------------------------------------------
@main.route('/cart-page', methods=["GET", "POST"])
def cart_page_viwes():
    if request.method == "GET":
        # 先判断是否登录
        # if 'id' in session and 'lognname' in session:
        # 1. 获取当前订单号,及订单里的数据
        # order_id = session['order_id']
        # goods_id = session["goods_id"]
        goodsid = [10001, 10002, 10003, 10004]
        goods = []
        i = 1
        for g in goodsid:
            good = Goods_info().query.filter_by(id=g).all()
            goods.append(good)
            i += 1
        # 2.传送到页面上
        numcount = i

        return render_template('cart-page.html', params=locals())
    else:
        create_time = datetime.now().strftime('%Y%m%d%H%M%S')

        # shop_id = session['shop_id']
        shop_id=1010
        user_id=2
        # user_id = session['user_id']
        # order_id = session['order_id']
        order = Order()
        order_details = Order_details()
        today = datetime.now().strftime('%Y-%m-%d')
        boday = '2019-01-16'
        todaynum = db.session.query(Order.order_id).filter(Order.create_time.like("%"+today+"%")).count()+1
        order_id =create_time+str(shop_id)+str(todaynum)
        print(order_id)
        list = request.form

        dict = list.to_dict(flat=False)
        goods_id = dict['good_info_id']
        goods_num = dict['qtybutton']
        remark = dict['test']
        print(goods_id, goods_num)
        i = 0
        pay_money =0
        for id in goods_id:
            # 插入表中B-order表
            # order_id；格式：年月日(8)+商家id(4)+时分秒(6)+订单号(2)
            # shop_id,user_id,pay_money,create_time
            order.order_id = order_id
            order.shop_id = shop_id
            order.user_id = user_id
            order.pay_money = pay_money
            order.create_time = create_time

            db.session.add(order)
            db.session.commit()
            # 插入表中A-order_details
            # 循环插入
            # order_id goods_id,goods_name,image_url,price,num,count_money
            goodsinfo = Goods_info.query.filter_by(id=id).first()
            order_details.order_id = order_id

            order_details.goods_id = goodsinfo.id
            order_details.goods_name = goodsinfo.goods_name
            order_details.image_url = goodsinfo.goods_image
            order_details.price =goodsinfo.goods_price
            print(goodsinfo.goods_price)
            order_details.num =goods_num[i]
            print(goods_num[i])
            order_details.count_money = int(goods_num[i])*int(goodsinfo.goods_price)
            pay_money+=order_details.count_money
            db.session.add(order_details)
            db.session.commit()

            i+=1
        # return redirect('/checkout')
        return '接收成功'