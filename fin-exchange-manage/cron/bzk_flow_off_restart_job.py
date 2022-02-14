import traceback
from datetime import datetime

import requests

import config
from infra.enums import PayloadReqKey


class BzkFlowOffRestartData:

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
        self.restart_time_check: bool = False
        self.request_time_check: bool = False

    def get_info(self):
        return self.__dict__


data = BzkFlowOffRestartData()


def notify_new_request(payload: dict):
    path: str = PayloadReqKey.name.get_val(payload)
    if 'flow_off_restart_info' in path:
        return
    data.lastRequestAt = datetime.now()


def check_and_restart():
    data.checkCount += 1
    data.lastCheckAt = datetime.now()
    dif_restart = datetime.now() - data.lastRestartAt
    dif_request = datetime.now() - data.lastRequestAt
    data.dif_restart_seconds = dif_restart.seconds
    data.dif_request_seconds = dif_request.seconds
    data.restart_time_check = data.dif_restart_seconds > 15 * 60
    data.request_time_check = data.dif_request_seconds > 11 * 60
    if data.restart_time_check and data.request_time_check:
        _trigger_restart()


def _trigger_restart():
    try:
        print('restart')
        restart_url = config.env('bzk-flow-restart-url')
        data.lastBecauseRequestAt = data.lastRequestAt.isoformat()
        data.lastRestartAt = datetime.now()
        data.restartCount += 1
        requests.get(url=restart_url)
        data.lastRestartResp = "restarted"
        print('restart end')
    except Exception as e:  # work on python 3.x
        data.lastException = {
            '__error_type': str(type(e)),
            'msg': str(e),
            'traceback': traceback.format_exc()
        }


def check():
    print('check='+ str(data.checkCount))
    check_and_restart()
