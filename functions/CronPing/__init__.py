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
msgQueue: func.Out[typing.List[str]] = None

def main(mytimer: func.TimerRequest, msg: func.Out[typing.List[str]]) -> None:
    msgQueue = msg

    for host in hosts:
        ping(host[0],host[1],host[2])

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
    report(out)
    # if out["status"] != "ok":
    #     report(out)

def report(result):
    msgQueue.set(result)