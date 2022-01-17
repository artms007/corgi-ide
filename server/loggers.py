# -*- coding: utf-8 -*-

# import logging
# import requests

import os
import logging
import requests

# try:
#     import logging
# except ModuleNotFoundError:
#     os.system('pip install logging')
# try:
#     import requests
# except ModuleNotFoundError:
#     os.system('pip install requests')

class SlackHandler(logging.StreamHandler):

    def __init__(self, url):
        super(SlackHandler, self).__init__()
        self.url = url

    def emit(self, record):
        msg = self.format(record)
        self.send_message(msg)

    def send_message(self, text):
        message = {
            'text': text,
        }

        requests.post(self.url, json=message)


def SlackLogger(WEB_HOOK_URL):
    # logging.basicConfig(
    #     level = logging.DEBUG,
    #     # format = "%(relativeCreated)08d[ms] - %(name)s - %(levelname)s - %(processName)-10s - %(threadName)s -\n*** %(message)s"
    # )
    slack_handler = SlackHandler(WEB_HOOK_URL)
    formatter = logging.Formatter('%(relativeCreated)08d[ms] - %(name)s - %(levelname)s - %(processName)-10s - %(threadName)s -\n*** %(message)s')
    slack_handler.setFormatter(formatter)
    slack_handler.setLevel(logging.DEBUG)
    logger = logging.getLogger("pyls_jsonrpc")
    logger.addHandler(slack_handler)


def ConsoleLogger():
    # # logのファイル
    logging.basicConfig(
        # handlers = [
        #     logging.FileHandler(
        #     filename = FILE_PATH,
        #     encoding='utf-8',
        #     mode='a+'
        #     )
        # ],
        level = logging.DEBUG,
        format = "%(relativeCreated)08d[ms] - %(name)s - %(levelname)s - %(processName)-10s - %(threadName)s -\n*** %(message)s"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    log = logging.getLogger("pyls_jsonrpc")
    log.addHandler(console)


def ConsoleLogger2(FILE_PATH):
    # # logのファイル
    logging.basicConfig(
        handlers = [
            logging.FileHandler(
            filename = FILE_PATH,
            encoding='utf-8',
            mode='a+'
            )
        ],
        level = logging.DEBUG,
        format = "%(relativeCreated)08d[ms] - %(name)s - %(levelname)s - %(processName)-10s - %(threadName)s -\n*** %(message)s"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    log = logging.getLogger("pyls_jsonrpc")
    log.addHandler(console)