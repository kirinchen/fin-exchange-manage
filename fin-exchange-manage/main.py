# main.py

import config
import exchange
from cron import cron_settings
from infra import database
from model import init_data

from rest.proxy_controller import get_flask_app
from service import sync_cron

app = get_flask_app()

database.init_db()
init_data.init_all_data()
exchange.load_all_service()
sync_cron.init_bind_all()
cron_settings.start_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=config.env_bool('debug'), port=9282, threaded=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# See http://docs.jinkan.org/docs/flask/patterns/sqlalchemy.html

# See https://www.maxlist.xyz/2019/11/10/flask-sqlalchemy-setting/
