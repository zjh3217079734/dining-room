# 当前程序的初始化
# 1.创建flask应用(app)以及各种配置
# 2.创建SQLALCHEMY的应用实例(db);


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 声明SQLAlchemy的实例
db = SQLAlchemy()  # 原来是:db = SQLAlchemy()


# 创建一个函数
def Create_App():
    # 创建Flask程序实例--app
    app = Flask(__name__,
                # template_folder="templates",  # 指定存放模板的文件夹名称,默认为templates
                static_url_path="/assets",  # "指定访问静态资源的路径
                static_folder="assets"  # 静态文件夹名称
                )

    # 为app指定各种配置
    app.config['DEBUG'] = True

    # 为app指定数据库的配置
    # 账号:root,密码:123456,数据库:project
    # 如果你的配置不一样,请输入自己的配置
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/project"
    app.config['SQLALCHEMY_COMMIT_ON_TEAROWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 配置session所需要的secret_key
    app.config['SECRET_KEY'] = "FeiShiBuKe"
    # 关联db以及app
    db.init_app(app)
    # 并将main蓝图与app关联到一起(让app托管main)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)  # 关联main蓝图

    # 返回已经创建好的程序实例app
    return app
