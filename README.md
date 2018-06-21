# twitter-fetcher

## Instalacion

### Python 3.6

Basico

`sudo add-apt-repository ppa:deadsnakes/ppa`

`sudo apt-get update`

`sudo apt-get install python3.6`

Otro

[Usar google :)](https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get)

### Virtualenv

Basico

`[sudo] pip install virtualenv`

[Mas detallado](https://virtualenv.pypa.io/en/stable/installation/)

## Setup

1. Clonar repo `https://github.com/JFNFJ/twitter-fetcher`
2. Entrar al repo `cd path/to/repo`
3. Armar entorno virtual `virtualenv -p python3.6 ./`
4. Activar entorno virtual `source bin/activate`
5. Instalar dependencias `pip install -r requirements.txt`
6. Desactivar entorno virtual `deactivate` (por si quieren saber)

### Flask

1. Setear variables de entorno para flask `FLASK_APP=api.py` `FLASK_ENV=development`
2. Levantar servidor `flask run`
3. Otra forma `python api.py`

### Redis

Cuando se le pega al endpoint `/track?topic="Salud"` se empieza a publicar en un canal `twitter:salud:stream` 
asi que recomiendo levantar un `redis-cli` y suscribirlo a `twitter:salud:stream`
 
## Documentacion

### General

* [Flask](http://flask.pocoo.org/docs/1.0/)
* [Python](https://docs.python.org/3/)
* [Redis](https://redis.io/documentation)
* [Twitter](https://developer.twitter.com/en/docs)

### Packages

* [redis-py](https://redis-py.readthedocs.io/en/latest/)
* [tweepy](http://tweepy.readthedocs.io/en/v3.5.0/)
* [python-twitter](https://python-twitter.readthedocs.io/en/latest/getting_started.html)
* [GeoText](http://geotext.readthedocs.io/en/latest/installation.html)
* [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
