FROM alpine:latest
LABEL maintainer Prasanta Kakati <prasantakakati@ekata.social>
RUN apk update && \
    apk add build-base linux-headers postgresql-client postgresql-dev \
    libpq python3 python3-dev jpeg-dev zlib-dev libressl-dev libffi-dev curl
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN mkdir /hashtagapp-api
WORKDIR /hashtagapp-api
COPY pyproject.toml poetry.lock /hashtagapp-api/
RUN source $HOME/.poetry/env && \
    poetry config settings.virtualenvs.create false && \
    poetry install --no-dev
COPY . /hashtagapp-api
CMD [ "sh", "start.sh" ]
