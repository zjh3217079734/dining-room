# 启动和管理项目的相关代码
from client import db, Create_App
from client.models import *
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

# 调用create_app得到app实例
app = Create_App()
# 创建Manager实例用于托管app
manager = Manager(app)
# 创建Migrate对象用于关联要管理的app和db
migarate = Migrate(app, db)
# 再通过Manager对象增加db迁移指令
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    # 使用Manager实例来启动程序
    manager.run()
