FROM python:3.6

#
# Install basic tools
#
RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip nginx vim git apt-transport-https

#
# Install node
#
ENV NVM_DIR /usr/local/nvm
RUN mkdir -p $NVM_DIR
ENV NODE_VERSION 9.11.1

RUN curl -s https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default && npm install -g npm

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update -y > /dev/null && apt-get install -y yarn

ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

#
# Build frontend
#

ENV FRONT_PATH /frontend

RUN git clone https://github.com/JFNFJ/frontend.git $FRONT_PATH
WORKDIR $FRONT_PATH

RUN npm install --silent
RUN yarn install

RUN npm run build

#
# Build API
#
COPY ./ /api
WORKDIR /api

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
RUN pip3 install --trusted-host pypi.python.org uwsgi

COPY ./nginx.conf /etc/nginx/sites-enabled/default

CMD service nginx start && uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=api:app