# 处理与客户相关的路由和视图
import math
from . import main
from .. import db
from hashlib import sha1
from ..models import *
from flask import Flask, render_template, request, session, redirect, make_response, url_for
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
# 首页需要判断cookies中是否有登录信息,不然会报错
# 根据网络ip获取所在城市
@main.route("/SelectCity")
def SelectCity():
    city = request.args["city"]
    cityid = Area.query.filter_by(area_name=city).all()
    return cityid


# -------------------------------------------
# -----------------------------------------------------------
# 应巧

# @main.route('/')
# def index_views():
#     if 'username' in request.cookies:
#         username = request.cookies['username']
#         return render_template('index.html', params=locals())
#     elif 'username' in session:
#         username = session['username']
#         return render_template('index.html', params=locals())
#     else:
#         return render_template('index.html', params={})

# 获取用户名
def get_name():
    if 'username' in session:
        username = session['username']
        return username
    else:
        return None


@main.route('/register', methods=['GET', 'POST'])
def register_views():
    username = get_name()
    if request.method == 'GET':
        return render_template('login-register.html', params={})
    else:
        username = request.form['uname']
        upwd = request.form['upwd']
        s = sha1()
        s.update(upwd.encode())
        password = s.hexdigest()
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
    username = get_name()
    url = request.headers.get('Referer', '/')
    # print(url)
    resp = redirect(url)
    # print("resp:",resp)
    # print(request.cookies)
    if 'username' in request.cookies:
        resp.delete_cookie('username')
    elif 'username' in session:
        session.clear()
        # print(request.cookies)
    return resp


@main.route('/login', methods=['GET', 'POST'])
def login_views():
    username = get_name()
    if request.method == 'GET':
        url = request.headers.get('Referer', '/')
        session['url'] = url
        if 'username' in session:
            return redirect(url)
            username = session['username']
            return render_template('index.html', params=locals())
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
        upwd = request.form['password']
        s = sha1()
        s.update(upwd.encode())
        password = s.hexdigest()
        user = User.query.filter_by(
            user_name=username, password=password).first()
        # print(user)
        # print(user.user_id)
        if user:
            session['id'] = user.user_id
            session['username'] = username
            url = session['url']
            # print("URL是:",url)
            resp = redirect(url)
            # print("resp是:::",resp)
            if 'isSaved' in request.form:
                resp.set_cookie('username', username, 60 * 60 * 24 * 365 * 10)
            return resp
        else:
            errMsg = "用户名或密码不正确"
            resp = make_response(render_template('login-register.html', params=locals()))
            resp.delete_cookie('username')
            return resp


@main.route('/resetpwd', methods=['GET', 'POST'])
def resetpwd_views():
    username = get_name()
    if request.method == 'GET':
        # print(1)
        return render_template('ResetPwd.html', params={})
    else:
        username = request.form['username']
        # print(username)
        npwd = request.form['newpassword']
        # print(npwd)

        s = sha1()
        s.update(npwd.encode())
        password = s.hexdigest()
        number = request.form['number']
        user = User.query.filter_by(user_name=username, phone=number).first()
        # print(user)
        if user:
            user.password = password
            user.create_time = datetime.now()
            user.update_time = datetime.now()

            db.session.add(user)
            db.session.commit()
            return "密码修改成功，请重新登录"
        else:
            return "用户名和手机号不匹配，请重试"


# 这个是之前的,暂时没用了...
# @main.route('/register', methods=['GET', 'POST'])
# def register_views():
#     username = get_name()
#     if request.method == 'GET':
#         return render_template('login-register.html', params={})
#     else:
#         username = request.form['uname']
#         upwd = request.form['upwd']
#         s = sha1()
#         s.update(upwd.encode())
#         password = s.hexdigest()
#         phone = request.form['uphone']
#
#         user = User()
#         user.user_name = username
#         user.password = password
#         user.phone = phone
#         user.sex = 'M'
#         user.create_time = datetime.now()
#         user.update_time = datetime.now()
#
#         try:
#             db.session.add(user)
#             db.session.commit()
#             return render_template('index.html', params=locals())
#         except Exception as ex:
#             print(ex)
#             return "注册失败，请联系管理员！"
#
#
# @main.route('/logout')
# def logout_views():
#     username = get_name()
#     url = request.headers.get('Referer', '/')
#     # print(url)
#     resp = redirect(url)
#     # print("resp:",resp)
#     # print(request.cookies)
#     if 'username' in request.cookies:
#         resp.delete_cookie('username')
#     elif 'username' in session:
#         session.clear()
#         # print(request.cookies)
#     return resp

#
# @main.route('/login', methods=['POST', 'GET'])
# def login_views():
#     if request.method == 'GET':
#         url = request.headers.get('Referer', '/')
#         session['url'] = url
#         # return render_template('login-register.html')
#         if 'username' in session:
#             return redirect(url)
#         else:
#             if 'username' in request.cookies:
#                 username = request.cookies['username']
#                 users = User.query.all()
#                 if username in users:
#                     session['username'] = username
#                     return redirect(url)
#                 else:
#                     resp = make_response(
#                         render_template(
#                             'login-register.html',
#                             params={}))
#                     resp.delete_cookie('username')
#                     return resp
#             else:
#                 return render_template('login-register.html', params={})
#     else:
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(
#             user_name=username, password=password).first()
#         if user:
#             session['id'] = user.user_id
#             session['username'] = username
#             url = session['url']
#             resp = redirect(url)
#             if 'isSaved' in request.form:
#                 resp.set_cookie('username', username, 60 * 60 * 24 * 365 * 10)
#             return resp
#         else:
#             errMsg = "用户名或密码不正确"
#             return render_template('login-register.html', params=locals())
#

# @main.route('/register/checkuname')
# def checkuname():
#     uname = request.args['uname']
#     users = User.query.filter_by(user_name=uname).all()
#     if users:
#         return "1"
#     else:
#         return "0"

# -----------------------------------------------------------


@main.route('/cart-page', methods=["GET", "POST"])
def cart_page_viwes():
    username = get_name()
    if request.method == "GET":
        # 先判断是否登录
        # if 'id' in session and 'lognname' in session:
        # 1. 获取当前订单号,及订单里的数据
        # order_id = session['order_id']
        goodsid = session["goods_id"]
        # goodsid = [10001, 10002, 10003, 10004]
        goods = []
        i = 1
        for goodid in goodsid:
            good = Goods().query.filter_by(id=goodid).all()
            goods.append(good)
            i += 1
        # 2.传送到页面上
        numcount = i

        return render_template('cart-page.html', params=locals())
    else:
        create_time = datetime.now().strftime('%Y%m%d%H%M%S')
        shop_id = session['shop_id']
        user_id = session['user_id']
        # shop_id = 2
        # user_id = 2
        order = Order()
        order_details = Order_details()
        today = datetime.now().strftime('%Y-%m-%d')
        boday = '2019-01-16'
        todaynum = db.session.query(Order.create_time).filter(
            Order.create_time.like("%" + today + "%")).count() + 1
        tm = ("%04d" % todaynum)
        sd = ("%06d" % shop_id)
        order_id = create_time + sd + tm
        # 获取表单数据并处理
        list = request.form
        dict = list.to_dict(flat=False)
        goods_id = dict['good_info_id']
        goods_num = dict['qtybutton']
        remark = dict['test']

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
            order_details = Order_details()

            # 插入表中A-order_details
            # 循环插入
            # order_id goods_id,goods_name,image_url,price,num,count_money
            goodsinfo = Goods.query.filter_by(id=gid).first()
            # last = db.session.query(Order_details).order_by(Order_details.id.desc()).first()
            # order_details.id = last.id + 1
            order_details.order_id = order_id
            order_details.goods_id = goodsinfo.id
            order_details.goods_name = goodsinfo.goods_name
            order_details.image_url = goodsinfo.goods_image
            order_details.price = goodsinfo.goods_price
            order_details.num = goods_num[i]
            order_details.count_money = int(goods_num[i]) * int(goodsinfo.goods_price)
            pay_money += order_details.count_money
            order.pay_money = pay_money
            db.session.add(order)
            db.session.add(order_details)
            db.session.commit()
            i += 1
        # return redirect('/checkout')
        return '接收成功'


# +---------------------
@main.route("/my-account", methods=["GET", "POST"])
def account_views():
    username = get_name()
    if request.method == "GET":
        #     user = User.query.filter_by(user_name="zhao").first()
        #     return render_template("my-account.html", user=user)
        #     判断是否登录成功
        if 'username' in session:
            print("username是:", username)
            user = User.query.filter_by(user_name=session['username']).first()
            return render_template('my-account.html', params=locals())
        # url = request.headers.get('Referer', '/')
        return redirect("/login")
    else:
        hidden = request.form.get('hid', '')
        print(hidden)
        if hidden == "Q":
            print('你好我们')
            name = request.form.get('uname', '')
            sex = request.form.get('usex', '')
            nick = request.form.get('unick', '')
            print(name)
            phone = request.form.get('uphone', '')
            # email=request.form.get('uphone','')
            # Email 和 quest.form.get('uemail','')
            # address=request.form.get('address','')
            # 创建user 对象 修改数据
            # user=Users.query.filter_by(user_id=session['id'])
            user = User.query.filter_by(user_name=name).first()
            user.user_name = name
            user.nick = nick
            user.phone = phone
            user.sex = sex
            # db.session.add(user)
            db.session.commit()
            return redirect('/my-account')
            # return "QueryOK"
        else:
            pwd1 = request.form.get('upwd1', '')
            pwd2 = request.form.get('upwd1', '')
            # 判断密码是否一致
            # result = check_password_hash(password, '123456')
            # print('这是测试的:',hidden)
            if pwd1 == pwd2:
                user = User()
                # sha1加密
                s = sha1()
                s.update(pwd1.encode())
                password = s.hexdigest()
                # password=hashlib.sha1(pwd1).hexdigest()
                # 前端加密方式
                # password = generate_password_hash(pwd1)
                user = User.query.filter_by(user_name='zhao').first()
                user.password = password
                # 添加 add  报错 数据库关系映射出错
                db.session.add(user)
                db.session.commit()
                return redirect('/my-account')
                # return "你好哈哈"


# -----------------------------------------------------------------------------
# 首页,直接跳转至这里了
# @main.route('/')
# @main.route('/index')
# def index_views():
#     username = get_name()
#     kws = request.args.get("kws", "")
#     if kws:
#         page = request.args.get("page", 1, type=int)
#         shops = db.session.query(Shop).filter_by(shop_name=kws).all()
#         totalCount = db.session.query(Shop).filter_by(shop_name=kws).count()
#     else:
#         page = request.args.get("page", 1, type=int)
#         shops = db.session.query(Shop).all()
#         totalCount = db.session.query(Shop).count()
#     kws1 = request.args.get("kws1", "")
#     if kws1:
#         page = request.args.get("page", 1, type=int)
#         shops = db.session.query(Shop.shop_name).filter(Shop.shop_name.like("%" + kws1 + "%")).all()
#         totalCount = db.session.query(Shop).filter(Shop.shop_name.like("%" + kws1 + "%")).count()
#     else:
#         page = request.args.get("page", 1, type=int)
#         shops = db.session.query(Shop).all()
#         totalCount = db.session.query(Shop).count()
#
#     pageSize = 10
#     ost = (page - 1) * pageSize
#     lastPage = math.ceil(totalCount / pageSize)
#     prevPage = 1
#     if page > 1:
#         prevPage = page - 1
#         nextPage = lastPage
#     if page < lastPage:
#         nextPage = page + 1
#
#     likes = db.session.query(Shop).limit(10).all()
#     classifies = db.session.query(Classify).all()
#     goods = db.session.query(Goods.goods_name).group_by(
#         "goods_name").order_by(func.count(Goods.shop_id).desc()).all()
#     return render_template("index.html", params=locals())

@main.route('/', methods=["GET", "POST"])
@main.route('/index', methods=["GET", "POST"])
@main.route("/shops", methods=["GET", "POST"])
def shops_views():
    classifies = db.session.query(Classify).all()
    goods = db.session.query(Goods).group_by(Goods.goods_name).order_by(func.count(Goods.shop_id).desc()).all()
    page = request.args.get("page",1,type=int)
    pageSize = 10
    ost = (page - 1) * pageSize
    shops = db.session.query(Shop).limit(pageSize).offset(ost).all()
    totalCount = db.session.query(Shop).count()
    lastPage = math.ceil(totalCount / pageSize)
    prevPage = 1
    if page > 1:
        prevPage = page - 1
    nextPage = lastPage
    if page < lastPage:
        nextPage = page + 1
    return render_template("index.html", params=locals())

@main.route("/release", methods=["GET", "POST"])
def release_views():
    username = get_name()
    if request.method == "GET":
        if "id" in session and "loginname" in session:
            loginname = session["loginname"]
            return render_template(("index.html"), params=locals())
        return render_template("index.html")

@main.route("/keywords", methods=["GET", "POST"])
def keywords_views():
    classifies = db.session.query(Classify).all()
    goods = db.session.query(Goods).group_by(Goods.goods_name).order_by(func.count(Goods.shop_id).desc()).all()
    page = request.args.get("page", 1, type=int)
    kws1 = request.args.get("kws1", "")
    url = "/keywords"
    pageSize = 10
    ost = (page - 1) * pageSize
    shops = db.session.query(Shop).filter(Shop.shop_name.like("%"+kws1+"%")).limit(pageSize).offset(ost).all()
    totalCount = db.session.query(Shop).filter(Shop.shop_name.like("%"+kws1+"%")).count()
    lastPage = math.ceil(totalCount / pageSize)
    prevPage = 1
    if page > 1:
        prevPage = page - 1
    nextPage = lastPage
    if page < lastPage:
        nextPage = page + 1
    return render_template("keywords-child.html", params=locals())

@main.route("/classify", methods=["GET", "POST"])
def classify_views():
    classifies = db.session.query(Classify).all()
    goods = db.session.query(Goods).group_by(Goods.goods_name).order_by(func.count(Goods.shop_id).desc()).all()
    classify_id = request.args.get("id")
    url = "/classify"
    shopid = db.session.query(Classify_shop).filter_by(classify_id=classify_id).all()
    shops = []
    for si in shopid:
        shop = db.session.query(Shop).filter_by(id=si.shop_id).first()
        shops.append(shop)
    totalCount = db.session.query(Shop).filter_by(id=si.shop_id).count()
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
    return render_template("classify-child.html",params=locals())

@main.route("/hotTag", methods=["GET", "POST"])
def tag_views():
    classifies = db.session.query(Classify).all()
    goods = db.session.query(Goods).group_by(Goods.goods_name).order_by(func.count(Goods.shop_id).desc()).limit(5).all()
    goodsname = request.args.get("goods")
    url = "/hotTag"
    shopid = db.session.query(Goods).filter_by(goods_name = goodsname).all()
    print(shopid[0].shop_id)
    shops = []
    for si in shopid:
        shop = db.session.query(Shop).filter_by(id=si.shop_id).first()
        shops.append(shop)
    totalCount = db.session.query(Shop).filter_by(id=si.shop_id).count()
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
    return render_template("/hottag.html", params=locals())

@main.route("/search", methods=["GET", "POST"])
def search_views():
    l = []
    kws = request.args.get("kws", "")
    if kws != '':
        results = db.session.query(Shop.id,Shop.shop_name).filter(
            Shop.shop_name.like("%" + kws + "%")).limit(4).all()
        print(results)
        for r in results:
            dic = {
                "id":r[0],
                "shopname":r[1]
            }
            l.append(dic)
    print(l)
    jsonStr = json.dumps(l)
    return jsonStr


# -----------------------------------------------------------
# 颜飞龙

@main.route('/checkout')
def checkout():
    username = get_name()
    # 检测用户登录
    session['id'] = 1
    if 'username' in request.cookies:
        username = request.cookies['username']

    if 'id' in session:
        uid = session['id']
        # 订单列表
        order = Order.query.filter_by(user_id=uid).all()
        # 订单列表字典,键为订单id
        odds = {}
        # 商店字典,键为订单id
        shops = {}

        for od in order:
            shop = Shop.query.filter_by(id=od.shop_id).first()
            order_details = Order_details.query.filter_by(order_id=od.order_id).all()
            odds[od.order_id] = order_details
            shops[od.order_id] = shop
        return render_template('checkout.html', params=locals())

    else:
        redirect(url_for('login_views'))


@main.route('/checkoutajax', methods=['POST'])
def checkoutajax():
    username = get_name()
    status = request.form['status']
    if status == '未付款':
        status = 0
    elif status == '已付款':
        status = 1
    else:
        status = 2
    print(status)
    session['id'] = 1
    if 'username' in request.cookies:
        username = request.cookies['username']

    if 'id' in session:
        uid = session['id']
        # 订单列表
        if status == 0:
            order = Order.query.filter_by(user_id=uid, status=0).all()
        elif status == 1:
            order = Order.query.filter_by(user_id=uid, status=1).all()
        else:
            order = Order.query.filter(Order.user_id == uid, Order.status != 0, Order.status != 1).all()
        # 订单列表字典,键为订单id
        odds = {}
        # 商店字典,键为订单id
        shops = {}

        for od in order:
            shop = Shop.query.filter_by(id=od.shop_id).first()
            order_details = Order_details.query.filter_by(order_id=od.order_id).all()
            odds[od.order_id] = order_details
            shops[od.order_id] = shop
        return render_template('checkoutpost.html', params=locals())

    else:
        redirect(url_for('login_views'))


@main.route('/remove', methods=['POST'])
def remove():
    username = get_name()
    order_id = request.form['remove']
    order = Order.query.filter_by(order_id=order_id).first()
    order.status = 4
    db.session.commit()
    return redirect(url_for('main.checkout'))


@main.route('/zhifu', methods=['POST'])
def zhifu():
    username = get_name()
    order_id = request.form['zhifu']
    order = Order.query.filter_by(order_id=order_id).first()
    order.status = 1
    db.session.commit()
    return redirect(url_for('main.checkout'))


#
# # 刘光辉 商品分类
# @main.route('/goods')
# def goods_views():
#     shop_id = request.args['id']
#     shop = Shop.query.filter_by(id=shop_id).first()
#     # 商品分类列表
#     # Menu.query.filter_by(shop_id=shop_id).all()
#     # 所有商品列表
#     menu_id = request.args.get('menu_id', '')
#     pageSize = 9
#     page = request.args.get('page', '1')
#     page = int(page)
#     ost = (page - 1) * pageSize
#     if menu_id:
#         menu = db.session.query(Menu).filter_by(id=menu_id).first()
#         goods = db.session.query(Goods).filter(Goods.menu_id == menu.id, Goods.goods_status == 1).limit(
#             pageSize).offset(ost).all()
#         # 对应商店里能显示的商品总数
#         totalCount = db.session.query(Goods).filter(Goods.menu_id == menu.id, Goods.goods_status == 1).count()
#     else:
#         menus = shop.shop_menu
#         l = []
#
#         for menu in menus:
#             l.append(menu.id)
#         # 商品分页
#         goods = db.session.query(Goods).filter(Goods.menu_id.in_(l), Goods.goods_status == 1).limit(pageSize).offset(
#             ost).all()
#         # 对应商店里能显示的商品总数
#         totalCount = db.session.query(Goods).filter(Goods.menu_id.in_(l), Goods.goods_status == 1).count()
#     # 最后一页页码
#     lastPage = math.ceil(totalCount / pageSize)
#     # 设置上一页默认为 1
#     prevPage = 1
#     if page > 1:
#         prevPage = page - 1
#
#     nextPage = lastPage
#     if page < lastPage:
#         nextpage = page + 1
#
#     return render_template('/shop.html', params=locals())
#
# ------------------------------------------------------------
# 刘光辉 商品分类
@main.route('/goods')
def goods_views():
    username = get_name()
    shop_id = request.args.get('id')
    shop = Shop.query.filter_by(id=shop_id).first()
    # 商品分类列表
    # Menu.query.filter_by(shop_id=shop_id).all()
    # 所有商品列表
    menu_id = request.args.get("menu_id", "")
    menus = shop.shop_menu
    pageSize = 9
    page = request.args.get('page', '1')
    page = int(page)
    ost = (page - 1) * pageSize
    if menu_id:
        menu = db.session.query(Menu).filter_by(id=menu_id).first()
        goods = db.session.query(Goods).filter(Goods.menu_id == menu.id, Goods.goods_status == 1).limit(
            pageSize).offset(ost).all()
        totalCount = db.session.query(Goods).filter(Goods.menu_id == menu.id, Goods.goods_status == 1).count()
    # 对应商店里能显示的商品总数
    else:
        l = []
        for menu in menus:
            l.append(menu.id)
            # 商品分页
        goods = db.session.query(Goods).filter(Goods.menu_id.in_(l), Goods.goods_status == 1).limit(pageSize).offset(
            ost).all()
        # 对应商店里能显示的商品总数
        totalCount = db.session.query(Goods).filter(Goods.menu_id.in_(l), Goods.goods_status == 1).count()
    # 最后一页页码
    lastPage = math.ceil(totalCount / pageSize)
    # 设置上一页默认为 1
    prevPage = 1
    if page > 1:
        prevPage = page - 1
    nextPage = lastPage
    if page < lastPage:
        nextpage = page + 1

    return render_template('/shop.html', params=locals())


# --------------------------------------------------------------------
# ----------------------------------------------------------------
# shop.html中的购物车按钮
@main.route('/goodslookup')
def gouwuche_views():
    username = get_name()
    if "good" in session:
        good = session["good"]
    else:
        good = []
    shop_id = request.args["shop_id"]
    session['shop_id'] = shop_id
    goods_id = request.args['goods_id']
    if goods_id in good:
        return ('已添加过购物车')
    good.append(goods_id)
    session["good"] = good
    print(session["good"])
    return ('添加购物车成功')
