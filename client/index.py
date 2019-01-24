from flask import Flask, render_template

app = Flask(__name__,
            # template_folder="",  # 指定存放模板的文件夹名称
            static_url_path="/assets",  # "指定访问静态资源的路径
            static_folder="assets"  # 静态文件夹名称
            )


@app.route("/")
@app.route("/<name>")
def html(name=None):
    if name is None:
        return render_template("index.html")
    return render_template(name)


if __name__ == "__main__":
    app.run(debug=True,
            # port=5555,  # 开放访问的端口号,默认为50000
            # host="0.0.0.0"  # host:指定访问到本项目的地址,0.0.0.0表示局域网内任何机器都可以访问到当前本项目,其他访问班级项目时需要使用ip地址
            )
