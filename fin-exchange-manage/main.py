# main.py

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import config
import exchange
from infra import database
from model import init_data

from rest.proxy_controller import get_flask_app
from service import sync_cron
from service.product_dao import ProductDao

app = get_flask_app()

database.init_db()
init_data.init_all_data()
exchange.load_all_service()
sync_cron.init_bind_all()

if __name__ == "__main__":
    # with database.session_scope() as session:
    #     p_dao: ProductDao = exchange.gen_impl_obj('binance', ProductDao,session)
    #     p_e = p_dao.get_by_item_symbol('BTC', 'USDT')
    #     print(p_e)

    app.run(host='0.0.0.0', debug=config.env_bool('debug'), port=9282, threaded=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# See http://docs.jinkan.org/docs/flask/patterns/sqlalchemy.html

# See https://www.maxlist.xyz/2019/11/10/flask-sqlalchemy-setting/
