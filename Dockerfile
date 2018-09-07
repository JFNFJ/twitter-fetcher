FROM python:3.6

RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip nginx vim

COPY ./ ./app
WORKDIR ./app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
RUN pip3 install --trusted-host pypi.python.org uwsgi

COPY ./nginx.conf /etc/nginx/sites-enabled/default

CMD service nginx start && uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=api:app