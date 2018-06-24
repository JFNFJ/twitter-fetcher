from flask import Flask, request
from multiprocessing import Process
from TwitterFetcher import TwitterFetcher
import os
import signal
import datetime
from settings import app


@app.route("/track", methods=['GET'])
def track():
    topic = request.args.get('topic')
    end = request.args.get('end') or datetime.date.today()
    lang = request.args.get('lang')
    app.logger.debug("Topic: %s\tEnding: %s\tLang: %s", topic, end, lang)
    p = init_process(target=start_fetching, args=(topic, end, lang))
    app.logger.debug("Process: %s", p.pid)
    return str(f'Topic: {topic} Ending: {end} Fetch: {p.pid}')


@app.route("/finish", methods=['GET'])
def finish():
    pid = int(request.args.get('process'))
    app.logger.debug("Process: %d", pid)
    os.kill(pid, signal.SIGTERM)
    return str(f'Finished: {pid}')


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
