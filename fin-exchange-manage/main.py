# main.py

import config
import exchange
from cron import cron_settings

from rest.proxy_controller import get_flask_app

app = get_flask_app()

exchange.load_all_service()
cron_settings.start_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=config.env_bool('debug'), port=9282, use_reloader=False, threaded=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# See http://docs.jinkan.org/docs/flask/patterns/sqlalchemy.html

# See https://www.maxlist.xyz/2019/11/10/flask-sqlalchemy-setting/
