import os
import json
import signal
import datetime
import jwt
from flask import request
from multiprocessing import Process
from TwitterFetcher import TwitterFetcher
from settings import app
from oauth import default_provider
from models.models import User
from flask_sqlalchemy import SQLAlchemy

oauth = default_provider(app)
db = SQLAlchemy(app)
EXPIRATION_HOURS = 24


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
    user = User.create_user(req['name'], req['email'], req['password'])
    app.logger.debug("User: %s", user)
    return str(f"Sign up {req} {url}")


@app.route("/login", methods=['POST'])
def login():
    req = request.get_json(force=True)
    app.logger.debug("Request: %s", req)
    name = req["name"]
    if not name:
        return json.dumps({'error': 'Nombre de usuario o email', 'code': 400}), 400
    password = req["password"]
    if not password:
        return json.dumps({'error': 'Una clave debe ser provista', 'code': 400}), 400
    user = User.query.filter_by(name=name).first()
    if not user or not user.validate_password(password):
        return json.dumps({'error': 'Usuario o clave incorrectos', 'code': 400}), 400

    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(hours=EXPIRATION_HOURS)
    token = jwt.encode({'name': user.name, 'exp': expiration_date}, app.secret_key, algorithm='HS256')

    return json.dumps({'name': name, 'token': token.decode('utf-8')}), 200


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
