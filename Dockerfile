FROM python:3.8-alpine
LABEL maintainer Prasanta Kakati <prasantakakati1994@gmail.com>
RUN apk update && \
    apk add build-base curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN mkdir /hashtagapp-back
WORKDIR /hashtagapp-back
COPY pyproject.toml poetry.lock /hashtagapp-back/
RUN . $HOME/.poetry/env && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY . /hashtagapp-back
CMD [ "sh", "start.sh" ]
