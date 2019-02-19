# 启动和管理项目的相关代码
from client import db, Create_App
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

# 导入所有的实体类方便实用db指令
# from .client.main.views import models, Create_App, db

# 调用Create_app得到app的实例
app = Create_App()

# 创建Manage实例用于托管app
manage = Manager(app)
# 创建Migrate对象用于关联要管理的app和db
migarte = Migrate(app, db)
# 在通过Manager对象增加db迁移指令
manage.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manage.run()
