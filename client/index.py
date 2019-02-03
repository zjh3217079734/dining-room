from flask import Flask, request, render_template, redirect
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
import pymysql


app = Flask(__name__,
            # template_folder="",  # 指定存放模板的文件夹名称
            static_url_path="/assets",  # "指定访问静态资源的路径
            static_folder="assets"  # 静态文件夹名称
            )
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/project"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
print(db)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


#++++++++++++++++++++++++++++++++++++++++++
# 各种表的类
# ........................................
# 门店申请表
class Apply(db.Model):
    pass

# ........................................
# 地区表
class Area(db.Model):
    pass


# ........................................
# 商品种类表 关联了门店id
class Category_goods(db.Model):
    pass



# ........................................
# 商品信息表
class Goods_info(db.Model):
    pass


# ........................................
# 商品种类表 关联了门店id
class Goods_type(db.Model):
    pass


# ........................................
# 商家账号信息
class Merchant(db.Model):
    pass


# ........................................
# 门店信息和商户信息关联的表
class Merchant_shop(db.Model):
    pass



# ........................................
# 订单信息表
class Order(db.Model):
    pass



# ........................................
#订单详情表，订单的详情主要就是购买商品的信息，通过订单的id来实现关联
class Order_details(db.Model):
    pass


# ........................................
# 门店信息表
class Shop_info(db.Model):
    pass



# ........................................
# 用来区分门店的类型
# 例如：中餐，西餐，汉堡，披萨，炸鸡
class type(db.Model):
    pass

# ........................................
# 类型和门店关联的表；
# 门店可以属于多个类型；
# 例如：汉堡王，可以是汉堡，也可以是西餐
class type_shop(db.Model):
    pass
# 这张表可以不要把? 通过映射就可以实现tpye和shop_info关联-蒋励
# ........................................
# 用户信息表
class user_info(db.Model):
    pass

# ........................................
#+++++++++++++++++++++++++++++++++++++++++


#---------------------------------------------
# localhost:5000/
# 主页部分
@app.route("/")
@app.route("/<name>")
def html(name=None):
    if name is None:
        return render_template("index.html")
    return render_template(name)
#-------------------------------------------

#----------------------------------------
# localhost:5000/cart-page.html
# 购物车后台部分
@app.route('/cart-page')
def cart_page_viwes():
    # 1. 获取当前订单号
    order_id = request.args['order_id']
    # 2. 根据订单号,查询出订单下菜品详情
    goods = db.session.query(order_details)
    pass

#---------------------------------------
if __name__ == "__main__":
    # app.run(debug=True,
    #         # port=5555,  # 开放访问的端口号,默认为50000
    #         # host="0.0.0.0"  # host:指定访问到本项目的地址,0.0.0.0表示局域网内任何机器都可以访问到当前本项目,其他访问班级项目时需要使用ip地址
    #         )

    manager.run()
