# twitter-fetcher

![LUL](https://i.kym-cdn.com/photos/images/newsfeed/001/290/930/5c3.jpg)

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

### Flask-SQLAlchemy

#### Migration

1. Activar entorno `source bin/activate`
2. Levantar una consola de python `python`
3. Importar models `from models.models import db`
4. Migrar models `db.create_all()`

#### Variables de entorno

* POSTGRESQL_DB (ejemplo `test_db`)
* POSTGRESQL_HOST (ejemplo `localhost`)
* POSTGRESQL_USER (ejemplo `postgres`)
* POSTGRESQL_PASSWORD (ejemplo `postgres`)
* POSTGRESQL_PORT (ejemplo `5432`)

### pytest

* Correr `pytest test`

### Redis

Cuando se le pega al endpoint `/track?topic="Salud"` se empieza a publicar en un canal `twitter:stream` 
asi que recomiendo levantar un `redis-cli` y suscribirlo a `twitter:stream`. Todos los fetchers terminan 
publicando en el mismo stream. 

#### Docker & redis 
```bash
docker run -d -p 6379:6379 --name redis redis:latest
docker start redis
docker port redis # debería devolver los puertos expuestos por el container (6379)
docker run -it --link redis:redis --rm redis redis-cli -h redis -p 6379 # Levanta un redis-cli
docker stop redis
```
 

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
* [pytest](https://docs.pytest.org/en/latest/)
* [Bot-O-Meter](https://github.com/IUNetSci/botometer-python)
