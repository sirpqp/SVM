import os

from flask import Flask, render_template, request, jsonify
from settings import *
from mysqldb.mysql import MySqlClient


conn = MySqlClient(db_configure={'host': HOST, 'user': USER, 'password': PWD, 'database': DATABASE})


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/part-input', methods=["GET", "POST"])
def part_input():
    args = request.args.to_dict()
    input_type = args.get('input-type')

    if request.method == "POST":
        args = request.form.to_dict()
        conn.save_item(args, 'svw_information')
        print(args)

    return render_template(f"part-input-{input_type}.html")


@app.route('/project-management', methods=['GET', 'POST'])
def project_management():
    if request.method == "GET":

        return render_template("management.html")

    if request.method == "POST":
        args = request.form.to_dict()
        args['carline'] = ','.join(request.form.getlist('carline'))

        conn.save_item(args, 'project_management')

    return 'ok'


@app.route('/load-project')
def load_project():
    result = conn.runquery("SELECT project,sop,tma FROM project_management")
    project = [p.get('project') for p in result]
    sop = [p.get('sop') for p in result]
    tma = [p.get('tma') for p in result]
    return jsonify({'project': project, 'sop': sop, 'tma': tma})


if __name__ == '__main__':
    app.run()
