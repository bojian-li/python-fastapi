import logging
import os
import sys
import time
import traceback
from datetime import datetime


def get_runtime_path() -> str:
    return os.path.join(os.getcwd(), 'runtime')


def get_data_path(path: str) -> str:
    return os.path.join(get_runtime_path(), 'data', path)


def get_log_path() -> str:
    return os.path.join(get_runtime_path(), 'log')


init_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - request_id:%(request_id)s - %(message)s")
datestr = time.strftime("%Y-%m", time.localtime())
log_path = get_log_path()
path = os.path.join(log_path, datestr)
if not os.path.isdir(path):
    os.makedirs(path)
accessFile = "{0}/{1}.log".format(path, datetime.today().day)
errorFile = "{0}/{1}_error.log".format(path, datetime.today().day)


def traceback_msg():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    info_list = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
    return ''.join(info_list)


class AppLyException(Exception):
    def __init__(self, message='', code=401, url=''):
        self.code = code
        self.message = message
        self.url = url

    def __str__(self):
        self.message = self.message.strip()
        return f"code:{self.code} - url:{self.url} - message:{self.message}:"

    def traceback_msg(self):
        return traceback_msg()
