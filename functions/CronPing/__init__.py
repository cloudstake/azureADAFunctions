import datetime
import logging
import subprocess
import os

import azure.functions as func

hosts = [
    ("north-america.relays-new.cardano-mainnet.iohk.io",None,None),
    ("north-america.relays-new.cardano-mainnet.iohk.io",None,None),
]

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    for host in hosts:
        ping(host)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

def ping(host: string, port: int = None, magic: string = None):
    args = ["./bin/cncli", "ping","--host",host]
    if port != None:
        args.append("--port")
        args.append(port)
    if magic != None:
        args.append("--magic")
        args.append(magic)
    result = subprocess.run(args,capture_output=True)
    out = json.loads(result.stdout);
    if out.status != "ok":
        report(out)

def report(result):
