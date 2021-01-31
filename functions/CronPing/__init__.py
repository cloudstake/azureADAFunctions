import datetime
import logging
import subprocess
import os
import json
import typing

import azure.functions as func

hosts = [
    ("north-america.relays-new.cardano-mainnet.iohk.io",None,None),
    ("north-america.relays-new.cardano-mainnet.iohk.io",None,None),
]
queue: typing.List[str] = list()

def main(mytimer: func.TimerRequest, msg: func.Out[typing.List[str]]) -> None:

    for host in hosts:
        ping(host[0],host[1],host[2])
    if len(queue) > 0:
        msg.set(queue)

def ping(host: str, port: int = None, magic: str = None):
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
        queue.append("Host: {0} Status: {}".format(result["host"], result["status"]))    