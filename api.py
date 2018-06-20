from flask import Flask, request
from multiprocessing import Process
from TwitterFetcher import TwitterFetcher
import os
import signal

app = Flask(__name__)


@app.route("/track", methods=['GET'])
def track():
    topic = request.args.get('topic')
    end = request.args.get('end')
    lang = request.args.get('lang')
    app.logger.debug("Topic: %s\tEnding: %s\tLang: %s", topic, end, lang)
    p = Process(target=start_fetching, args=(topic, end, lang))
    p.daemon = True
    p.start()
    app.logger.debug("Process: %s", p.pid)
    return str(f'Topic: {topic} Ending: {end} Fetch: {p.pid}')


@app.route("/finish", methods=['GET'])
def finish():
    pid = int(request.args.get('process'))
    app.logger.debug("Process: %d", pid)
    os.kill(pid, signal.SIGTERM)
    return str(f'Finished: {pid}')


def start_fetching(topic, end='2018-06-09', lang='es'):
    twitter_fetcher = TwitterFetcher()
    twitter_fetcher.stream(topic, languages=[lang])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
