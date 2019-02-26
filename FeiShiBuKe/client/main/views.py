# 处理与客户相关的路由和视图

from . import main
from .. import db
from hashlib import sha1
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
# from flask_paginate import Pagination, get_page_parameter
import json


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
        # user_id = session['user_id']
        # order_id = session['order_id']
        shop_id = 2
        user_id = 2
        order = Order()
        order_details = Order_details()
        today = datetime.now().strftime('%Y-%m-%d')
        boday = '2019-01-16'
        todaynum = db.session.query(Order.create_time).filter(
            Order.create_time.like("%" + today + "%")).count() + 1
        tm=("%04d"%todaynum)
        sd=("%06d"%shop_id)
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
@main.route("/my-account",methods=["GET","POST"])
def account_views():
    if request.method == "GET":
        user = User.query.filter_by(user_name="zhao").first()
        return render_template("my-account.html",user=user)
        #判断是否登录成功
        # if 'id' in session and 'loginname' in session:
        #     user = User.query.filter_by(user_id=session['id']).first()
        #     return render_template('my-acount.html',user)
        # url= request.headers.get('Referer', '/')
        # return redirect(url)
    else:
        hidden=request.form.get('hid','')
        print(hidden)
        if hidden == "Q":
            print('你好我们')
            name= request.form.get('uname','')
            sex = request.form.get('usex','')
            nick= request.form.get('unick','')
            print(name)
            phone=request.form.get('uphone','')
            # email=request.form.get('uphone','')
            #Email 和 quest.form.get('uemail','')
            # address=request.form.get('address','')
            #创建user 对象 修改数据
            #user=Users.query.filter_by(user_id=session['id'])
            user=User.query.filter_by(user_name=name).first()
            user.user_name=name
            user.nick=nick
            user.phone=phone
            user.sex=sex
            # db.session.add(user)
            db.session.commit()
            return redirect('/my-account')
            # return "QueryOK"
        else:
            pwd1=request.form.get('upwd1','')
            pwd2=request.form.get('upwd1','')
            # 判断密码是否一致
            #result = check_password_hash(password, '123456')
            # print('这是测试的:',hidden)
            if pwd1 == pwd2:
                user=User()
                # sha1加密
                s = sha1()
                s.update(pwd1.encode())
                password = s.hexdigest()
                # password=hashlib.sha1(pwd1).hexdigest()
                #前端加密方式
                # password = generate_password_hash(pwd1)
                user=User.query.filter_by(user_name='zhao').first()
                user.password=password
                #添加 add  报错 数据库关系映射出错
                db.session.add(user)
                db.session.commit()
                return redirect('/my-account')
                # return "你好哈哈"





# -----------------------------------------------------------------------------
@main.route("/release", methods=["GET", "POST"])
def release_views():
    if request.method == "GET":
        if "id" in session and "loginname" in session:
            loginname = session["loginname"]
            return render_template(("index.html"), params=locals())
        return render_template("index.html")


@main.route("/shop", methods=["GET", "POST"])
def shops_views():
    page = request.args.get('page', 1, type=int)
    if request.args.get("shop_id"):
        pagination = db.session.query(Shop).filter_by(
            shop_id=id).paginate(page, per_page=10)
    else:
        pagination = db.session.query(Shop).paginate(page, per_page=10)
    shops = pagination.items
    return render_template("index.html", pagination=pagination, shops=shops)


@main.route("/rightSideTag", methods=["GET", "POST"])
def tag_views():
    menus = db.session.query(Menu).all()
    counts = menus.count()
    goods = db.session.query(Goods).limit(7).all()
    return render_template("/index.html", params=locals())


@main.route("/search", methods=["GET", "POST"])
def search_views():
    l = []
    kws = request.args.get("kws", "")
    if kws != '':
        results1 = db.session.query(Goods.goods_name).filter(
            Goods.goods_name.like("%" + kws + "%")).all()
        results2 = db.session.query(Menu.menu_name).filter(
            Menu.menu_name.like("%" + kws + "%")).all()
        results3 = db.session.query(Shop.shop_name).filter(
            Shop.shop_name.like("%" + kws + "%")).all()
        for result in [results1, results2, results3]:
            for r in result:
                l.append(r[0])
    jsonStr = json.dumps(l)
    return jsonStr


#-------------------------------------------------------------------
#刘光辉 商品分类
@main.route('/goods')
def goods_views():
    shop_id = request.args['shop_id']
    shop = Shop.query.filter_by(id=shop_id).first()
    #商品分类列表
     #Menu.query.filter_by(shop_id=shop_id).all()
        
        
    #所有商品列表

    menu_id = request.args.get('menu_id','')
    pageSize = 9
    page = request.args.get('page','1')
    page = int(page)
    ost = (page-1) * pageSize
    if menu_id:
        menu = db.session.query(Menu).filter_by(id=menu_id).first()
        goods = db.session.query(Goods).filter(Goods.menu_id==menu.id,Goods.goods_status==1).limit(pageSize).offset(ost).all()
    # 对应商店里能显示的商品总数
        totalCount = db.session.query(Goods).filter(Goods.menu_id==menu.id,Goods.goods_status==1).count()
    else:
        menus = shop.shop_meun
        l = []
   
        for menu in menus:
            l.append(menu.id)
    # 商品分页
        goods = db.session.query(Goods).filter(Goods.menu_id.in_(l),Goods.goods_status==1).limit(pageSize).offset(ost).all()
    # 对应商店里能显示的商品总数
        totalCount = db.session.query(Goods).filter(Goods.menu_id.in_(l),Goods.goods_status==1).count()
    # 最后一页页码
    lastPage = math.ceil(totalCount / pageSize)
    # 设置上一页默认为 1
    prevPage = 1
    if page > 1:
        prevPage = page - 1
    
    nextPage = lastPage
    if page < lastPage:
        nextpage = page +1

    return render_template('/shop.html',params=locals())
#-------------------------------------------------------------------
# shop.html中的购物车按钮
@main.route('/goodslookup')
def gouwuche_views():
    shop_id = request.args["shop_id"]
    goods_id = request.args['goods_id']
    goodids=[]
    goodids.append(goods_id)
    session["goods_id"] = goods_id
    print(session)
    print(goodids)
    return "('添加购物车成功')"

#----------------------------------------------------------------























# -----------------------------------------------------------
# 颜飞龙

@main.route('/checkout')
def checkout():
    session['id'] = 1
    if 'username' in request.cookies:
        username = request.cookies['username']

    if 'id' in session:
        uid = session['id']
        order = Order.query.filter_by(user_id=uid).all()
        odds = {}
        shops = {}
        for od in order:
            shop = Shop.query.filter_by(id=od.shop_id).first()
            order_details = Order_details.query.filter_by(order_id=od.order_id).all()
            odds[od.order_id] = order_details
            shops[od.order_id] = shop
        return render_template('checkout.html',params=locals())
    else:
        redirect(url_for('login_views'))

@main.route('/remove')
def remove():
    pass


#------------------------------------------------------------
#刘光辉 商品分类
@main.route('/goods')
def goods_views():
    shop_id = request.args['shop_id']
    shop = Shop.query.filter_by(id=shop_id).first()
    #商品分类列表
    menus = shop.shop_meun #Menu.query.filter_by(shop_id=shop_id).all()
    #所有商品列表
    l = []
    # if request.args['goods_type']:
    #    l.append(request.args['goods_type'])
    # else:
    for menu in menus:
        l.append(menu.id)
    # 商品分页
    pageSize = 9
    page = request.args.get('page','1')
    page = int(page)

    ost = (page-1) * pageSize
    goods = db.session.query(Goods).filter(Goods.menu_id.in_(l),Goods.goods_status==1).limit(pageSize).offset(ost).all()
    # 对应商店里能显示的商品总数
    totalCount = db.session.query(Goods).filter(Goods.menu_id.in_(l),Goods.goods_status==1).count()
    # 最后一页页码
    lastPage = math.ceil(totalCount / pageSize)
    # 设置上一页默认为 1
    prevPage = 1
    if page > 1:
        prevPage = page - 1
    
    nextPage = lastPage
    if page < lastPage:
        nextpage = page +1

    return render_template('/shop.html',params=locals())

@main.route('/goodslookup')
def gouwuche_views():
    goods_id = request.args['goodsid']
    goodids=[]
    goodids.append(goods_id)
    session['goods_id'] = goodids
    cb=request.args['callback']
    print(goodids)
    return cb+"('添加购物车成功')"
#-------------------------------------------------------------------

