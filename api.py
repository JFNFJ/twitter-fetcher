from flask import Flask, request
from multiprocessing import Process
from TwitterFetcher import TwitterFetcher
import os
import json
import signal
import datetime
from settings import app


@app.route("/track", methods=['POST'])
def track():
    req = request.get_json(force=True)
    app.logger.debug("Request: %s", req)
    p = init_process(target=start_fetching, args=(req["topic"], req["end"], req["lang"]))
    response = {"topic": req["topic"], "end": req["end"], "lang": req["lang"], "process": p.pid}
    app.logger.debug("Response: %s", response)
    return json.dumps(response)


@app.route("/finish", methods=['POST'])
def finish():
    req = request.get_json(force=True)
    app.logger.debug("Process: %s", req)
    os.kill(req["process"], signal.SIGTERM)
    response = {"process": req["process"], "status": "killed"}
    return json.dumps(response)


def start_fetching(topic, end=datetime.date.today(), lang='es'):
    twitter_fetcher = TwitterFetcher()
    twitter_fetcher.stream(topic, languages=[lang])


def init_process(target, args):
    p = Process(target=target, args=args)
    p.daemon = True
    p.start()
    return p


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
