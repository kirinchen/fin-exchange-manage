import traceback
from datetime import datetime

import requests

import config


class BzkFlowOffRestart:

    def __init__(self):
        self.lastRequestAt = datetime.now()
        self.lastBecauseRequestAt = None
        self.lastRestartAt = datetime.now()
        self.lastCheckAt = None
        self.restartCount = 0
        self.checkCount = 0
        self.lastException: dict = None
        self.lastRestartResp: str = None

    def notify_new_request(self):
        self.lastRequestAt = datetime.now()

    def check_and_restart(self):
        self.checkCount += 1
        self.lastCheckAt = datetime.now()
        dif_restart = datetime.now() - self.lastRestartAt
        if dif_restart.seconds < 17 * 60:
            return
        dif_request = datetime.now() - self.lastRequestAt
        if dif_request.seconds < 12 * 60:
            return
        self.restart()

    def restart(self):
        try:
            print('restart')
            restart_url = config.env('bzk-flow-restart-url')
            resp = requests.get(url=restart_url)
            self.lastBecauseRequestAt = self.lastRequestAt.isoformat()
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
