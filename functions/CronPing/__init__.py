import datetime
import logging
import subprocess
import os
import json
import typing

import azure.functions as func
from pip._vendor import requests

hosts = [
    ("north-america.relays-new.cardano-mainnet.iohk.io",None,None),
]
dataToQueue = list()

def main(mytimer: func.TimerRequest, config) -> None:

    TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    configObj = json.loads(config.read())
    TELEGRAM_CHATS = configObj["telegramRecipients"]
    # logging.info(TELEGRAM_CHATS)
    # logging.info(configObj["hosts"][0])
    for host in configObj["hosts"]:
        ping(host["host"],host["port"],host["magic"])
    if len(dataToQueue) > 0:
        for m in dataToQueue:
            send_message(m, TELEGRAM_CHATS, TELEGRAM_BOT_TOKEN)

        raise Exception("error")

def ping(host: str, port: str = None, magic: str = None):
    args = ["./bin/cncli", "ping","--host",host]
    if port != None:
        args.append("--port")
        args.append(port)
    if magic != None:
        args.append("--magic")
        args.append(magic)
    result = subprocess.run(args,capture_output=True)
    out = json.loads(result.stdout);
    logging.info(out)
    if out["status"] != "ok":
        dataToQueue.append("Host: {} Status: {}".format(out["host"], out["status"]))    

def send_message(message, TELEGRAM_CHATS, TELEGRAM_BOT_TOKEN):
    if TELEGRAM_CHATS.count(',') > 0:
        for chat in TELEGRAM_CHATS.split(','):
            logging.info(chat)
            send_message(message,chat,TELEGRAM_BOT_TOKEN)
    else:
        params = {
            'chat_id': TELEGRAM_CHATS,
            'text': message
        }
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        r = requests.get(url, params=params)
        if r.status_code == 200:
            print(json.dumps(r.json(), indent=2))
        else:
            r.raise_for_status()