# 根据数据库编写实体类
from . import db
#导入这个,用来使用功能Float精度
from sqlalchemy.dialects.mysql import FLOAT



# 商家账号表
class Merchant(db.Model):
    __tablename__ = "merchant"
    # 主键 商家的id号,主键,自增长值为10001,不为空
    id = db.Column(
        db.Integer, primary_key=True)
    #   '商家账号的用户名,不可超过20位,不为空
    name = db.Column(
        db.String(20), unique=True, index=True, nullable=False)
    #   '商家账号的密码,加密:40位,不为空
    passwd = db.Column(db.String(40), nullable=False)
    #   '商家版状态（0：商家主账号，1：子帐号，2：不开启)',不为空
    status = db.Column(db.Integer, default=0, nullable=False)
    #   '商家账号的手机号（非必填）'可为空
    phone = db.Column(db.String(11), nullable=True)
    # -------------关系映射---------------
    # 多对多映射的远程表名
    shops = db.relationship(
        "Shop",  # 远程表
        secondary="merchant_shop",  # 中间表
        lazy="dynamic",  # 实时获取
        backref=db.backref(
            "merchants",  # 本表的别名
            lazy="dynamic"  # 实时获取
        )
    )
    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 门店信息表
class Shop(db.Model):
    __tablename__ = "shop"
    # 门店id主键,自增长
    id = db.Column(
        db.Integer, primary_key=True)

    #    '门店名称',不为空',
    shop_name = db.Column(
        db.String(10), nullable=False)

    #    '门店图片',可以为空',
    shop_img = db.Column(
        db.String(100), nullable=True)

    #    '门店电话：默认为11位手机号，可以为空',
    shop_phone = db.Column(
        db.String(11), nullable=True)

    #    '门店状态（0：未注册，1：正常运行，2：审核中，3：未营业，4：商家已删除，不存在）',不为空
    shop_status = db.Column(
        db.Integer, default=0, nullable=False)

    #    '门店营业开始时间',
    shop_begin_time = db.Column(
        db.Time, nullable=True)

    #    '门店营业结束时间',
    shop_end_time = db.Column(
        db.Time, nullable=True)

    #    '门店标签；多个标签的话，以分号隔开',
    shop_tag = db.Column(
        db.String(100), nullable=True)

    #    '门店简介',
    shop_intro = db.Column(
        db.String(100), nullable=True)

    #    '所属地区',
    area = db.Column(
        db.String(10), nullable=True)
    # ----------下面都是关系映射------------------
    # "与菜单的外键关联映射"
    shop_meun = db.relationship(
        'Menu',
        backref='menu_shop',
        lazy='dynamic'
    )
    # 与商品表的关系映射
    shop_goods = db.relationship(
        'Goods',
        backref='goods_shop',
        lazy='dynamic'
    )
    # 与门店申请表的关系映射
    shop_apply = db.relationship(
        'Apply',
        backref='apply_shop',
        lazy='dynamic'
    )
    shop_order = db.relationship(
        'Order',
        backref='order_shop',
        lazy ='dynamic',
    )
    # 实现与Classify的关联关系(多对多,中间借助classify_shop关联表进行关联)

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 门店和商家关联表
class Merchant_shop(db.Model):
    __tablename__ = "merchant_shop"
    # 主键
    id = db.Column(
        db.Integer, primary_key=True)

    #   '商家账号id',不为空,外键为merchant表下的merchant_id
    #多对多在merchant表里面
    merchant_id = db.Column(db.Integer, db.ForeignKey("merchant.id"))

    #   '门店id',不为空,外键为shop表下的id
    #多对多在merchant表里面
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))
    #   '备注门店名',可为空
    remake_name = db.Column(
        db.String(50), nullable=True)

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 门店分类表 - -用来关联门店的种类
class Classify(db.Model):
    __tablename__ = "classify"

    # 类型id.主键,自增长
    id = db.Column(db.Integer, primary_key=True)

    # 类型名称,不为空
    classify_name = db.Column(db.String(10), nullable=False)
    # 与shop表的多对多
    shops = db.relationship(
        "Shop",  # 远程表
        secondary="classify_shop",  # 中间表
        lazy="dynamic",  # 实时获取
        backref=db.backref(
            "classifys",  # 本表的别名
            lazy="dynamic"  # 实时获取
        )
    )

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 类型和门店关联的表:
# 门店可以属于多个类型
# 例如：汉堡王，可以是汉堡，也可以是西餐';
class Classify_shop(db.Model):
    __tablename__ = "classify_shop"

    # 主键,自增长
    id = db.Column(db.Integer, primary_key=True)

    # 类型id.主键,自增长
        #多对多在classify表里面
    classify_id = db.Column(db.Integer, db.ForeignKey("classify.id"))

    # 类型名称,不为空
        #多对多在classify表里面
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 地区表
class Area(db.Model):
    __tablename__ = "area"
    # 主键,自增长
    id = db.Column(db.Integer, primary_key=True)
    # 城市id ,不为空
    area_id = db.Column(db.Integer, unique=True, nullable=False)
    # 城市名称,不为空
    area_name = db.Column(db.String(10), nullable=False)
    # 城市父类id,不为空
    area_pid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 用户信息表
class User(db.Model):
    __tablename__ = "user"
    #    '用户id',主键,自增长
    user_id = db.Column(db.Integer,  primary_key=True )
    #    '用户账号；默认用手机号，不得超过11位长度.并且不可重复',
    user_name = db.Column(db.String(11), nullable=False,unique=True, index=True)

    #    '用户密码；用哈希值存入',
    password = db.Column(db.String(40), nullable=False)

    #    '用户性别(''M'':男,默认,''F'',女)',
    sex = db.Column(db.Enum("M", "F"), default="M", nullable=False)
    #    '用户昵称(不得超过20个字符)',
    nick = db.Column(db.String(20), nullable=True)
    #    '用户手机号',
    phone = db.Column(db.String(11), nullable=True)
    #    '用户头像',
    image = db.Column(db.String(100), nullable=True)
    #    '创建时间',
    create_time = db.Column(db.DateTime, nullable=False)
    #    '更新时间',
    update_time = db.Column(db.DateTime, nullable=False)
    # --------------下面是关系映射----------------
    # 与order表的关系映射
    user_orders = db.relationship(
        'Order',
        backref='order_user',
        lazy='dynamic'
    )

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 商品菜单表
class Menu(db.Model):
    __tablename__ = "menu"

    # 主键,自增长
    id = db.Column(db.Integer, primary_key=True)

    # 菜单名称'菜品种类;例如：饮料，烤鸭，米饭等',非空
    menu_name = db.Column(db.String(10), nullable=False)

    # 门店id,多个菜单关联到一个门店
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 商品的信息表
class Goods(db.Model):
    __tablename__ = "goods"
    # 主键,自增长
    id = db.Column(db.Integer, primary_key=True)

    # '商品的门店id',
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))

    # 商品名称
    goods_name = db.Column(db.String(10), nullable=False)

    # '商品图片',
    goods_image = db.Column(db.String(100), nullable=False)

    # '商品单价',
    goods_price = db.Column(FLOAT(precision=10, scale=2), nullable=False)

    # '商品状态（默认为1：开启，0：未开启）',
    goods_status = db.Column(db.SmallInteger, nullable=False, default=1)

    # '商品备注；也就是商品简介',
    goods_notes = db.Column(db.String(100), nullable=True)
    # ------------关系映射------------------
    # 与订单详情表的关系映射
    good_datails = db.relationship(
        'Order_details',
        backref='good',
        lazy='dynamic'
    )

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 订单表
class Order(db.Model):
    __tablename__ = "order"
    # 主键,自增长
    id = db.Column(db.Integer, primary_key=True)

    # # '订单id；格式：年月日(8)+时分秒(6)+商家id(6)+订单号(4)',
    # 商家id不够6位的前面填充0
    order_id = db.Column(db.String(24), nullable=False,unique=True, index=True)

    # #   '门店id',
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))

    # #   '用户id',
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    # #   '支付金额',
    pay_money = db.Column(FLOAT(precision=10, scale=2), nullable=True)

    # #   '支付类型：0，现金，1：在线支付',
    pay_type = db.Column(db.SmallInteger, nullable=False, default=0)

    # #   '订单交易状态：默认为（0）；0：未付款，1：已付款，交易成功，2：交易失败，3：退款，4：删除订单',
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    # #   '商家订单删除状态：0：未删除，1：删除；默认为0；',
    shop_status = db.Column(db.SmallInteger, nullable=False, default=0)

    # #   '订单创建时间',
    create_time = db.Column(db.DateTime, nullable=False)

    # #   '订单更新时间',
    update_time = db.Column(db.DateTime, nullable=False)

    # #   '付款时间',
    pay_time = db.Column(db.DateTime, nullable=True)

    # #   '订单备注',
    remark = db.Column(db.String(100), nullable=True)

    # #   '桌号：默认为null； \r\n0：堂食；其他号码：桌号',
    table_id = db.Column(db.String(100), nullable=True)

    # #   '评价状态；0：未评价，1：已评价，2：删除评价',
    appraise_status = db.Column(db.SmallInteger, nullable=True, default=0)

    # #   '买家评价内容',
    appraise = db.Column(db.String(100), nullable=True)

    # #   '评分数值；',
    appraise_score = db.Column(db.SmallInteger, nullable=True, default=0)

    # #   '买家昵称是否匿名； 0：不匿名，1：匿名；默认为0',
    nick_status = db.Column(db.SmallInteger, nullable=True, default=0)

    # #   '买家昵称--用户id获取到的nick',匿名之后这里显示为:匿名
    nick = db.Column(db.String(20), nullable=True)

    # ----------关系映射-------------
    # 与详情表的映射
    orders_datails = db.relationship(
        'Order_details',
        backref='orders',
        lazy='dynamic'
    )

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 订单详情表
class Order_details(db.Model):
    __tablename__ = "order_details"
    # 主键,自增长
    id = db.Column(db.Integer, primary_key=True)

    # # '订单id；格式：年月日(8)+时分秒(6)+商家id(6)+订单号(4)',
    # 商家id不够6位的前面填充0
    order_id = db.Column(db.String(24), db.ForeignKey("order.order_id"))
    # #   '门店id',
    goods_id = db.Column(db.Integer, db.ForeignKey("goods.id"))

    # #   '商品名称',
    goods_name = db.Column(db.String(20), nullable=False)

    # #   '图片的url地址',
    image_url = db.Column(db.String(100), nullable=True)

    # #   '单价',
    price = db.Column(FLOAT(precision=10, scale=2), nullable=False, default=0)

    # #   商品数量
    num = db.Column(db.Integer, nullable=False, default=1)

    #   总价格
    count_money = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)


# 申请表
class Apply(db.Model):
    __tablename__ = "apply"
    # 主键,自增长
    id = db.Column(db.Integer, primary_key=True)

    # 申请门店id
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))

    # 申请门店名称
    shop_name = db.Column(db.String(10), nullable=False)

    # '申请门店图片',
    shop_img = db.Column(db.String(100), nullable=True)

    # '申请门店资格证明(营业执照图片)',
    shop_prove = db.Column(db.String(100), nullable=True)

    # '申请门店营业时间',
    shop_begin_time = db.Column(db.Time, nullable=True)

    # '申请门店结束时间',
    shop_end_time = db.Column(db.Time, nullable=True)

    # '申请状态',
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    # '申请备注',
    remark = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return "%s表创建好了" % (self.__class__.__name__)
