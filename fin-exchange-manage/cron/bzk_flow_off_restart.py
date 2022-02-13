import traceback
from datetime import datetime

import requests

import config
from infra.enums import PayloadReqKey


class BzkFlowOffRestart:

    def __init__(self):
        self.lastRequestAt = datetime.now()
        self.lastBecauseRequestAt = None
        self.lastRestartAt = datetime.now()
        self.lastCheckAt = None
        self.restartCount = 0
        self.checkCount = 0
        self.dif_restart_seconds = 0
        self.dif_request_seconds = 0
        self.lastException: dict = None
        self.lastRestartResp: str = None

    def notify_new_request(self, payload: dict):
        path: str = PayloadReqKey.name.get_val(payload)
        if 'flow_off_restart_info' in path:
            return
        self.lastRequestAt = datetime.now()

    def check_and_restart(self):
        self.checkCount += 1
        self.lastCheckAt = datetime.now()
        dif_restart = datetime.now() - self.lastRestartAt
        dif_request = datetime.now() - self.lastRequestAt
        self.dif_restart_seconds = dif_restart.seconds
        self.dif_request_seconds = dif_request.seconds
        restart_time_check: bool = self.dif_restart_seconds > 17 * 60
        request_time_check: bool = self.dif_request_seconds > 12 * 60
        if restart_time_check and request_time_check:
            self._trigger_restart()

    def _trigger_restart(self):
        try:
            print('restart')
            restart_url = config.env('bzk-flow-restart-url')
            self.lastBecauseRequestAt = self.lastRequestAt.isoformat()
            self.lastRestartAt = datetime.now()
            self.restartCount += 1
            resp = requests.get(url=restart_url)
            self.lastRestartResp = resp.text
            print('restart end')
        except Exception as e:  # work on python 3.x
            self.lastException = {
                '__error_type': str(type(e)),
                'msg': str(e),
                'traceback': traceback.format_exc()
            }

    def get_info(self):
        return self.__dict__
