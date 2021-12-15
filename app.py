import os

from flask import Flask, render_template, request
from settings import *


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index_1.html")


@app.route('/part-input', methods=["GET", "POST"])
def part_input():
    if request.method == "GET":
        return render_template("part-input_1.html")

    if request.method == "POST":
        args = request.args


if __name__ == '__main__':
    app.run()
