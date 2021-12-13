import os

from flask import Flask, render_template
from settings import *


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index_1.html")


if __name__ == '__main__':
    app.run()
