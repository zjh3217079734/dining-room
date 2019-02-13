from flask import Flask, render_template,request

from werkzeug.security import generate_password_hash,check_password_hash

# sorapoi
from checkout import add_new_route


app = Flask(__name__,
            # template_folder="",  # 指定存放模板的文件夹名称
            static_url_path="/assets",  # "指定访问静态资源的路径
            static_folder="assets"  # 静态文件夹名称
            )
 
# sorapoi
add_new_route(app)

@app.route("/")
@app.route("/<name>")
def html(name=None):
    if name is None:
        return render_template("index.html")
    return render_template(name)


# 应巧
@app.route('/login',methods=['GET','POST'])
def login_views():
	if request.method=='GET':
		return render_template('login-register.html')
	else:
		username=request.form['username']
		password=generate_password_hash(request.form['password'])
		print("用户名：%s,密码:%s"%(username,password))
		result=check_password_hash(password,'123456')
		if result:
			print('密码为123456')
		else:
			print('密码不是123456')
		return "接收数据成功"


@app.route('/register',methods=['GET','POST'])
def register_views():
	if request.method=='GET':
		return render_template('login-register.html')
	else:
		username=request.form['username']
		password=generate_password_hash(request.form['password'])
		email=request.form['email']
		print("用户名:%s,密码:%s,邮箱:%s"%(username,password,email))
		result=check_password_hash(password,'123456')
		if result:
			print('密码为123456')
		else:
			print('密码不是123456')
		return "接收数据成功"


if __name__ == "__main__":
    app.run(debug=True,
            # port=5555,  # 开放访问的端口号,默认为50000
            # host="0.0.0.0"  # host:指定访问到本项目的地址,0.0.0.0表示局域网内任何机器都可以访问到当前本项目,其他访问班级项目时需要使用ip地址
            )

