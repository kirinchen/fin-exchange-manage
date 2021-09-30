# main.py

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from infra import database

app = Flask(__name__)







@app.route('/')
def index():
    # Create data


    return 'ok'


if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# See http://docs.jinkan.org/docs/flask/patterns/sqlalchemy.html

# See https://www.maxlist.xyz/2019/11/10/flask-sqlalchemy-setting/
