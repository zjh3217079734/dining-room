# 处理与客户相关的路由和视图
import math
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
import json
# ---------------------------------------------
# localhost:5000/
# 主页部分


#这行代码是: 你给我什么,我重新把路由地址给你,不管你是什么东西
# @main.route("/<name>")
# def html(name=None):
#     return render_template(name)


# 根据网络ip获取所在城市
@main.route("/SelectCity")
def SelectCity():
    city = request.args["city"]
    print(city)
    print("leixing :", type(city))
    cityid = Area.query.filter_by(area_name=city).all()
    print("cityid:", cityid)
    return city

# -------------------------------------------
# -----------------------------------------------------------
# 应巧
# 首页需要判断cookies中是否有登录信息,不然会报错


@main.route('/')
def index_views():
    if 'username' in request.cookies:
        username = request.cookies['username']
        return render_template('index.html', params=locals())
    else:
        return render_template('index.html', params=None)


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
            session['id'] = user.user_id
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
        user.sex = 'M'
        user.create_time = datetime.now()
        user.update_time = datetime.now()
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
            good = Goods().query.filter_by(id=g).all()
            goods.append(good)
            i += 1
        # 2.传送到页面上
        numcount = i

        return render_template('cart-page.html', params=locals())
    else:
        create_time = datetime.now().strftime('%Y%m%d%H%M%S')

        # shop_id = session['shop_id']
        shop_id = 2
        user_id = 2
        # user_id = session['user_id']
        # order_id = session['order_id']
        order = Order()
        order_details = Order_details()
        today = datetime.now().strftime('%Y-%m-%d')
        boday = '2019-01-16'
        todaynum = db.session.query(Order.create_time).filter(
            Order.create_time.like("%"+today+"%")).count()+1
        order_id = create_time+str(shop_id)+str(todaynum)
        print(order_id)
        list = request.form

        dict = list.to_dict(flat=False)
        goods_id = dict['good_info_id']
        goods_num = dict['qtybutton']
        remark = dict['test']
        print(goods_id, goods_num)
        i = 0
        pay_money = 0
        # 插入表中B-order表
        # order_id；格式：年月日时分秒(8)+商家id+数量
        # shop_id,user_id,pay_money,create_time
        order.order_id = order_id
        order.shop_id = shop_id
        order.user_id = user_id
        order.pay_money = pay_money
        order.update_time = create_time
        order.create_time = create_time

        db.session.add(order)
        db.session.commit()
        for gid in goods_id:
            # db.session.flush()
            # 插入表中A-order_details
            # 循环插入
            # order_id goods_id,goods_name,image_url,price,num,count_money
            goodsinfo = Goods.query.filter_by(id=gid).first()
            # last = db.session.query(Order_details).order_by(Order_details.id.desc()).first()
            # print(last.id)
            # order_details.id = last.id+1
            order_details.order_id = order_id
            order_details.goods_id = goodsinfo.id
            order_details.goods_name = goodsinfo.goods_name
            order_details.image_url = goodsinfo.goods_image
            order_details.price = goodsinfo.goods_price
            print(goodsinfo.goods_price)
            order_details.num = goods_num[i]
            print(goods_num[i])
            order_details.count_money = int(
                goods_num[i])*int(goodsinfo.goods_price)
            pay_money += order_details.count_money
            order.pay_money = pay_money
            db.session.add(order)

            db.session.add(order_details)
            db.session.commit()

            i += 1
        # return redirect('/checkout')
        return '接收成功'


# -----------------------------------------------------------------------------
@main.route("/shops",methods=["GET","POST"])
def shops_views():
    kws = request.args.get("kws", "")
    if kws:
        page = request.args.get("page", 1, type=int)
        shops = db.session.query(Shop).filter_by(shop_name=kws).all()
        totalCount = db.session.query(Shop).filter_by(shop_name=kws).count()
    else:
        page = request.args.get("page", 1, type=int)
        shops = db.session.query(Shop).all()
        totalCount = db.session.query(Shop).count()
    kws1 = request.args.get("kws1","")
    if kws1:
        page = request.args.get("page", 1, type=int)
        shops = db.session.query(Shop.shop_name).filter(Shop.shop_name.like("%"+kws1+"%")).all()
        totalCount = db.session.query(Shop).filter(Shop.shop_name.like("%"+kws1+"%")).count()
    else:
        page = request.args.get("page", 1, type=int)
        shops = db.session.query(Shop).all()
        totalCount = db.session.query(Shop).count()

    pageSize = 10
    ost = (page - 1) * pageSize
    lastPage = math.ceil(totalCount / pageSize)
    prevPage = 1
    if page > 1:
        prevPage = page - 1
        nextPage = lastPage
    if page < lastPage:
        nextPage = page + 1

    likes = db.session.query(Shop).limit(10).all()
    classifies = db.session.query(Classify).all()
    goods = db.session.query(Goods.goods_name).group_by(
        "goods_name").order_by(func.count(Goods.shop_id).desc()).all()
    return render_template("index.html",params=locals())

@main.route("/release", methods=["GET", "POST"])
def release_views():
    if request.method == "GET":
        if "id" in session and "loginname" in session:
            loginname = session["loginname"]
            return render_template(("index.html"), params=locals())
        return render_template("index.html")

@main.route("/suggest",methods=["GET","POST"])
def suggest_views():
    kws = request.args.get("kws","")
    if kws:
        shops = db.session.query(Shop).filter_by(shop_name=kws).all()
    else:
        shops = db.session.query(Shop).all()
    return render_template("/pages",shops=shops)

@main.route("/keywords",methods=["GET","POST"])
def keywords_views():
    kws1 = request.args.get("kws1","")
    if kws1:
        shops = db.session.query(Shop.shop_name).filter(Shop.shop_name.like("%"+kws1+"%")).all()
    else:
        shops = []
    return render_template("/pages",shops=shops)

@main.route("/classify",methods=["GET","POST"])
def classify_views():
    likes = db.session.query(Shop).limit(10).all()
    classifies = db.session.query(Classify).all()
    goods = db.session.query(Goods.goods_name).group_by("goods_name").order_by(func.count(Goods.shop_id).desc()).all()
    classify_id = request.args.get("id")
    print(classify_id)
    shopid = db.session.query(Classify_shop).filter_by(classify_id=classify_id).all()
    print("shop_id:",shopid[0].shop_id)
    shops = []
    for si in shopid:
        shop = db.session.query(Shop).filter_by(id=si.shop_id).first()
        shops.append(shop)

    totalCount = db.session.query(Shop).count()
    page = request.args.get("page", 1, type=int)
    pageSize = 10
    ost = (page - 1) * pageSize
    lastPage = math.ceil(totalCount / pageSize)
    prevPage = 1
    if page > 1:
        prevPage = page - 1
        nextPage = lastPage
    if page < lastPage:
        nextPage = page + 1
    return render_template("index.html",params=locals())

@main.route("/hotTag", methods=["GET", "POST"])
def tag_views():
    goods_name = request.args.get("goods","")
    likes = db.session.query(Shop).limit(10).all()
    classifies = db.session.query(Classify).all()
    goods = db.session.query(Goods).group_by(
        "goods_name").order_by(func.count(Goods.shop_id).desc()).all()
    print(goods)
    shop_id = request.args.get("id")
    print(shop_id)
    # shops = []
    # for goodsname in goods:
    #     shopsid = db.session.query(Goods.shop_id).filter_by(goods_name=goodsname[0]).all()
    #     print(shopsid)
    #     shop = db.session.query(Shop).filter_by(id=shop_id).all()
    #     shops.append(shop)
    totalCount = db.session.query(Shop).count()
    page = request.args.get("page", 1, type=int)
    pageSize = 10
    ost = (page - 1) * pageSize
    lastPage = math.ceil(totalCount / pageSize)
    prevPage = 1
    if page > 1:
        prevPage = page - 1
        nextPage = lastPage
    if page < lastPage:
        nextPage = page + 1


    return render_template("/index.html", params=locals())

@main.route("/search", methods=["GET", "POST"])
def search_views():
    l = []
    kws = request.args.get("kws", "")
    if kws != '':
        # results1 = db.session.query(Goods.goods_name).filter(
        #     Goods.goods_name.like("%"+kws+"%")).limit(4).all()
        results2 = db.session.query(Shop.shop_name).filter(
            Shop.shop_name.like("%"+kws+"%")).limit(4).all()
        for result in [results2]:
            for r in result:
                l.append(r[0])
    jsonStr = json.dumps(l)
    return jsonStr
