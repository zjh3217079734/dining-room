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

@app.route("/")
@app.route("/<name>")
def html(name=None):
    if name is None:
        return render_template("index.html")
    return render_template(name)

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
