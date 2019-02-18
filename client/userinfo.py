#个人信息
from flask import Flask,render_template,requesst
from flask_sqlalchemy import SQLALchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

app = Flask(__name__)
#绑定数据库
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:123456@176.23.4.101:3306/project"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['DEBUG'] = True
#创建db
db = SQLALchemy(app)
manager = Manager(app)
migrate = Migrate(db,app)
#创建db属性由
manager.add_command('db',MigrateCommand)

#查看数据库信息
@app.route("/my_account",methods=['GET','POST'])
def my_account():
    if request.method == "GET":
        ueses = User_info.query.filter_by(id=session["id"])
        # name = info()
        # uname = Users.query(Users).filter_by(uname = name).first()
        # #判断是否登录
        # if uname.uname == name:
        #     user = db.session.query(user_info).filter_by(uname = name)all()
        #     name = user.uname
        #     phone=user
        #     return render_template("my_account.html")
        return render_template("my-account.html",params=localds())    
    else:
        name = request.from['uname']
        phone= request.from['phone']
        weix = request.from['weixin']
        zhif = request.from['zhifubao']
        emial= request.from['emial']
        addr = request.from['address']
        return "成功"

if __name__ == "__main__":
    manager.run()