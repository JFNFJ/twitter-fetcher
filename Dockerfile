#
# Build frontend
#
FROM node:8 as armacion
ENV FRONT_PATH /frontend

RUN git clone https://github.com/JFNFJ/frontend.git $FRONT_PATH
WORKDIR $FRONT_PATH
ENV NODE_PATH=./src
ENV PATH=$PATH:/node_modules/.bin
RUN yarn
RUN yarn build

#
# Build API
#
FROM python:3.6

#
# Install basic tools
#
RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip nginx vim git apt-transport-https

ENV FRONT_PATH /frontend
RUN mkdir $FRONT_PATH
COPY --from=armacion $FRONT_PATH/build $FRONT_PATH/build
COPY ./ /api
WORKDIR /api

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
RUN pip3 install --trusted-host pypi.python.org uwsgi

COPY ./nginx.conf /etc/nginx/sites-enabled/default

CMD service nginx start && uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=api:app