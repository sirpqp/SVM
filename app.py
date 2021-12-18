import pandas as pd
from hashlib import md5
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from settings import *
from mysqldb.mysql import MySqlClient

# 数据库连接，与数据库交互的操作类
conn = MySqlClient(db_configure={'host': HOST, 'user': USER, 'password': PWD, 'database': DATABASE})

app = Flask(__name__)


# 主页路由函数
@app.route('/')
def hello_world():
    return render_template("index.html")


# 零件录入页面
@app.route('/part-input', methods=["GET", "POST"])
def part_input():
    # 将get请求的参数转换成字典格式
    args = request.args.to_dict()
    # 当前录入页面的类型
    input_type = args.get('input_type')

    if request.method == "POST":
        try:
            # post请求时，将存入表单提交数据到数据库
            args = request.form.to_dict()

            # 提取上传的文件
            file = request.files.get('picture')
            file_path = file_process(file)

            # 将文件的相对路径作为picture字段的值存入数据库
            args.update({'picture': file_path})
            conn.save_item(args, 'svw_information')
        except Exception as e:
            return f'表单数据处理错误，错误信息: {e}'

    return render_template(f"part-input-{input_type}.html")


def file_process(file):
    if not file.filename:
        return
    # 时间戳+文件名 -> md5之后用作存储的新文件名
    file_name = md5((str(datetime.now()) + file.filename).encode('utf-8')).hexdigest()

    # 获取文件类型
    file_type = file.filename.split('.')[-1]

    # 组成文件存储的相对路径
    file_path = f'/static/img/upload/{file_name}.{file_type}'

    # 存储文件
    file.save(BASE_DIR + file_path)

    return file_path


# project管理页面
@app.route('/project-management', methods=['GET', 'POST'])
def project_management():
    if request.method == "GET":
        # 返回管理页面
        return render_template("management.html")

    if request.method == "POST":
        try:
            # post请求提交表单数据，并存入数据库
            args = request.form.to_dict()

            # carline字段为多选，需要单独处理
            args['carline'] = ','.join(request.form.getlist('carline'))

            conn.save_item(args, 'project_management')
        except Exception as e:
            return f'表单数据处理错误，错误信息: {e}'

        return 'ok'


# 加载project，sop，tma数据自动填充到表单输入页面
@app.route('/load-project')
def load_project():
    result = conn.runquery("SELECT project,sop,tma FROM project_management")
    project = [p.get('project') for p in result]
    sop = [p.get('sop') for p in result]
    tma = [p.get('tma') for p in result]
    return jsonify({'project': project, 'sop': sop, 'tma': tma})


@app.route('/part-query')
def part_query():
    return render_template('part-query.html')


@app.route('/load-project-information')
def load_project_information():
    args = request.args.to_dict()
    project = args.get('project')
    sop = args.get('lingjianhao')
    count = conn.runquery("SELECT COUNT(0) AS num FROM project_management WHERE project=%s AND sop=%s",
                          args=(project, sop))[0].get('num')
    if count:
        # 通过pandas从数据库读取数据，并进行转置，方便前端处理
        data = pd.read_sql_query(f"SELECT * FROM svw_information WHERE project='{project}' AND sop='{sop}'", conn)
        return {'msg': '查询成功', 'data': {'items': data.T.to_dict(), 'keys': data.keys().tolist()}, 'code': 200}
    else:
        return {'msg': '没有该项目或零件号，请确认', 'data': {}, 'code': 201}


if __name__ == '__main__':
    app.run()
