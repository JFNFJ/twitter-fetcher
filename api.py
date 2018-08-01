import os
import json
import signal
import datetime
from flask import request
from multiprocessing import Process
from TwitterFetcher import TwitterFetcher
from settings import app
from oauth import default_provider
from models.models import User

oauth = default_provider(app)


@app.route("/start_thread", methods=['POST'])
def track():
    req = request.get_json(force=True)
    app.logger.debug("Request: %s", req)
    p = init_process(target=start_fetching, args=(req["topic"], req["end"], req["lang"]))
    response = {"topic": req["topic"], "end": req["end"], "lang": req["lang"], "process": p.pid}
    app.logger.debug("Response: %s", response)
    return json.dumps(response)


@app.route("/finish_thread", methods=['POST'])
def finish():
    req = request.get_json(force=True)
    app.logger.debug("Request: %s", req)
    os.kill(req["process"], signal.SIGTERM)
    response = {"process": req["process"], "status": "killed"}
    return json.dumps(response)


@app.route("/sign_up", methods=['POST'])
def sign_up():
    req = request.get_json(force=True)
    app.logger.debug("Request: %s", req)
    user = User.create_user(req)
    app.logger.debug("User: %s", user)
    return str(f"Sign up {req} {url}")


@app.route("/login", methods=['POST'])
def login():
    req = request.get_json(force=True)
    app.logger.debug("Request: %s", req)
    # TODO
    return str("Login")


@app.route("/log_out", methods=['POST'])
def log_out():
    req = request.get_json(force=True)
    app.logger.debug("Request: %s", req)
    # TODO
    return str("Log out")


@app.route("/topic/<topic_id>/results", methods=['POST'])
def get_results(topic_id):
    req = request.get_json(force=True)
    app.logger.debug("Topic: %s,\tRequest: %s", topic_id, req)
    # TODO
    return str(f"Results {topic_id}")


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
