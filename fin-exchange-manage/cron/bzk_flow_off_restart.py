import traceback
from datetime import datetime

import requests

import config


class BzkFlowOffRestart:

    def __init__(self):
        self.lastRequestAt = datetime.now()
        self.lastRestartAt = datetime.now()
        self.restartCount = 0
        self.lastException: dict = None
        self.lastRestartResp: str = None

    def notify_new_request(self):
        self.lastRequestAt = datetime.now()

    def check_and_restart(self):
        dif_restart = datetime.now() - self.lastRestartAt
        if dif_restart.seconds < 11 * 60:
            return
        dif_request = datetime.now() - self.lastRequestAt
        if dif_request.seconds < 7 * 60:
            return

    def restart(self):
        try:
            print('restart')
            restart_url = config.env('bzk-flow-restart-url')
            resp = requests.get(url=restart_url)
            self.lastRestartResp = resp.text
            self.lastRestartAt = datetime.now()
            self.restartCount += 1
            print('restart end')
        except Exception as e:  # work on python 3.x
            self.lastException = {
                '__error_type': str(type(e)),
                'msg': str(e),
                'traceback': traceback.format_exc()
            }

    def get_info(self):
        return self.__dict__
