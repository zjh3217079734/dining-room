# 根据数据库编写实体类
from . import db


class Apply(db.Model):
    __tablename__ = "apply"
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    # 门店id
    shop_id = db.Column(db.Integer, nullable=False)
    # 门店名称
    shop_name = db.Column(db.String(255), nullable=False)
    # 门店图片
    shop_img = db.Column(db.String(255), nullable=True)
    # 门店资质证明（营业执照）
    shop_prove = db.Column(db.String(255), nullable=True)
    # 门店营业开始时间
    shop_begin_time = db.Column(db.DATE, nullable=True)
    # 门店营业结束时间
    shop_end_time = db.Column(db.DATE, nullable=True)
    # 门店标签
    shop_tag = db.Column(db.String(255), nullable=True)
    # 申请状态；0：申请中，1：已通过，2：已拒绝
    status = db.Column(db.SmallInteger, nullable=False)
    # 申请备注
    remark = db.Column(db.String(255), nullable=True)
    pass

# ........................................
# 地区表


class Area(db.Model):
    __tablename__ = "area"
    # 二级地区id
    area_id = db.Column(db.Integer, primary_key=True)
    # 二级地区名称
    area_name = db.Column(db.String(255), nullable=False)
    # 父地区id
    area_pid = db.Column(db.Integer, nullable=False)
    pass


# ........................................
# 商品种类表 关联了门店id
class Category_goods(db.Model):
    __tablename__ = "category_goods"
    id = db.Column(db.Integer, primary_key=True)
    # 商品种类
    category_name = db.Column(db.String(255), nullable=False)
    # 门店id
    shop_id = db.Column(db.Integer, nullable=False)
    pass


# ........................................
# 商品信息表
class Goods_info(db.Model):
    __tablename__ = "goods_info"
    id = db.Column(db.Integer, primary_key=True)
    # 商品名称
    goods_name = db.Column(db.String(255), nullable=False)
    # 商品图片
    goods_image = db.Column(db.String(255), nullable=False)
    # 商品单价
    goods_price = db.Column(db.Float(2), nullable=False)
    # 商品状态（默认为1：开启，0：未开启）
    goods_status = db.Column(db.SmallInteger, nullable=False)
    # 商品分类
    goods_type = db.Column(db.Integer, nullable=False)
    # 商品备注；也就是商品简介
    goods_notes = db.Column(db.String(255), nullable=True)
    pass


# ........................................
# 商品种类表 关联了门店id
class Goods_type(db.Model):
    __tablename__ = "goods_type"
    id = db.Column(db.Integer, primary_key=True)
    # 商品种类
    type_name = db.Column(db.String(255), nullable=False)
    # 门店id
    shop_id = db.Column(db.Integer)
    pass


# ........................................
# 商家账号信息
class Merchant(db.Model):
    __tablename__ = "merchant"
    merchant_id = db.Column(db.Integer, primary_key=True)
    merchant_name = db.Column(db.String(255), nullable=False)
    merchant_pwd = db.Column(db.String(255), nullable=False)
    # 商家版状态（0：商家主账号，1：子帐号，2：不开启)
    merchant_status = db.Column(db.Integer, primary_key=True)
    merchant_phone = db.Column(db.String(11), nullable=True)
    pass


# ........................................
# 门店信息和商户信息关联的表
class Merchant_shop(db.Model):
    __tablename__ = "merchant_shop"
    merchant_id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, nullable=False)
    remake_name = db.Column(db.String(255), nullable=True)
    pass


# ........................................
# 订单信息表
class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    # 订单id；格式：年月日(8)+商家id(4)+时分秒(6)+订单号(2)
    order_id = db.Column(db.String(30),
                         nullable=False,
                         )
    # 门店id
    shop_id = db.Column(db.Integer, db.ForeignKey('shop_info.id'),nullable=False)
    # userid
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'),nullable=False)
    # 支付金额
    pay_money = db.Column(db.Float(2), nullable=False)
    # 支付类型
    pay_type = db.Column(db.SmallInteger, nullable=True)
    # 订单交易状态
    status = db.Column(db.SmallInteger, nullable=True)
    # 订单创建时间
    create_time = db.Column(db.DATETIME, nullable=True)
    # 订单更新时间
    update_time = db.Column(db.DATETIME, nullable=True)
    # 付款时间
    pay_time = db.Column(db.DATETIME, nullable=True)
    # 订单备注
    remark = db.Column(db.String(255), nullable=True)
    # 桌号 0 外带；其他号码：桌号
    table_id = db.Column(db.Integer, nullable=True)
    # 评价状态；0：未评价，1：已评价，2：删除评价
    appraise_status = db.Column(db.Integer, nullable=True)
    # 评价内容
    appraise = db.Column(db.String(255), nullable=True)
    # 评分数值/获赞数值
    appraise_score = db.Column(db.SmallInteger, nullable=True)
    # 买家/用户昵称是否匿名； 0：不匿名，1：匿名；默认为0
    nick_status = db.Column(db.SmallInteger, nullable=True)
    # 买家/用户昵称（不得超过20个字符
    nick = db.Column(db.String(20), nullable=True)
    # 一 对 order_details('多')
    order_details = db.relationship(
        'Order_details',
        backref='order',
        lazy='dynamic'
    )


# ........................................
# 订单详情表，订单的详情主要就是购买商品的信息，通过订单的id来实现关联
class Order_details(db.Model):
    __tablename__ = "order_details"
    id = db.Column(db.Integer, primary_key=True)
    # 订单Id 增加外键,引用自order表的order_id主键
    order_id = db.Column(db.String(30),
                         db.ForeignKey('order.id'),
                         nullable=False,)
    # 商品id
    goods_id = db.Column(db.Integer, nullable=False)
    # 商品名称
    goods_name = db.Column(db.VARCHAR(255), nullable=False)
    # 图片url地址
    image_url = db.Column(db.VARCHAR(255), nullable=False)
    # 单价
    price = db.Column(db.Float, nullable=False)
    # 商品数量 不为空
    num = db.Column(db.Integer, nullable=False)
    # 订单总价
    count_money = db.Column(db.VARCHAR(255), nullable=True)


# ........................................
# 门店信息表
class Shop_info(db.Model):
    __tablename__ = "shop_info"
    id = db.Column(db.Integer, primary_key=True)
    # 门店名称
    shop_name = db.Column(db.String(255), nullable=False)
    # 门店图片
    shop_img = db.Column(db.String(255), nullable=True)
    # 门店电话：默认为11位手机号，可以为空
    shop_phone = db.Column(db.Integer, nullable=True)
    # 门店状态（0：未注册，1：正常运行，2：审核中，3：未营业，4：商家已删除，不存在）
    shop_status = db.Column(db.SmallInteger, nullable=False)
    # 门店营业开始时间
    shop_begin_time = db.Column(db.DATE, nullable=True)
    # 门店营业结束时间
    shop_end_time = db.Column(db.DATE, nullable=True)
    # 门店标签
    shop_tag = db.Column(db.String(255), nullable=True)
    # 门店简介
    shop_intro = db.Column(db.String(255), nullable=True)
    # 所属地区
    area = db.Column(db.Integer, nullable=False)
    order_id = db.relationship(
        'Order',
        backref='shop_info',
        lazy='dynamic'
    )

# ........................................
# 用来区分门店的类型
# 例如：中餐，西餐，汉堡，披萨，炸鸡
class Type(db.Model):
    __tablename__ = "type"
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(10), nullable=False)
    pass

# ........................................
# 类型和门店关联的表；
# 门店可以属于多个类型；
# 例如：汉堡王，可以是汉堡，也可以是西餐


class Type_shop(db.Model):
    __tablename__ = "type_shop"
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.Integer, nullable=False)
    pass

# ........................................
# 用户信息表


class User_info(db.Model):
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True)
    # 用户账号；默认用手机号，不得超过11位长度.并且不可重复
    user_name = db.Column(db.String(11), primary_key=True)
    # 用户密码；用哈希值存入
    password = db.Column(db.String(40), nullable=False)
    # 用户性别('M':男,默认,'F',女)
    sex = db.Column(db.Enum('M', 'F'), nullable=True)
    # 用户昵称(不得超过20个字符)
    nick = db.Column(db.String(20), nullable=True)
    # 用户手机号
    phone = db.Column(db.String(255), nullable=True)
    # 用户头像
    image = db.Column(db.String(255), nullable=True)
    # 用户所在区域
    user_area = db.Column(db.Integer, nullable=False)
    # 创建时间
    create_time = db.Column(db.DateTime, nullable=True)
    # 更新时间
    update_time = db.Column(db.DATETIME, nullable=True)
    order_user_id = db.relationship(
        'Order',
        backref='user_info',
        lazy='dynamic'

    )

# ........................................
# +++++++++++++++++++++++++++++++++++++++++
