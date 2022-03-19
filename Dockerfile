FROM python:3.8-alpine
LABEL maintainer Prasanta Kakati <prasantakakati1994@gmail.com>
RUN apk update && \
    apk add build-base linux-headers postgresql-client postgresql-dev \
    libpq python3 python3-dev jpeg-dev zlib-dev libressl-dev libffi-dev curl inkscape \
    terminus-font ttf-inconsolata ttf-dejavu font-noto ttf-font-awesome font-noto-extra \
    font-vollkorn font-misc-cyrillic font-mutt-misc font-screen-cyrillic font-winitzki-cyrillic font-cronyx-cyrillic \
    font-noto-thai font-noto-tibetan font-sony-misc font-daewoo-misc font-jis-misc \
    font-arabic-misc font-noto-arabic font-noto-armenian font-noto-cherokee \
    font-noto-devanagari font-noto-ethiopic font-noto-georgian font-noto-hebrew font-noto-lao font-noto-malayalam \
    font-noto-tamil font-noto-thaana font-noto-bengali
RUN wget https://fonts.google.com/download?family=Noto%20Sans%20JP -O 'noto-sans-jp.zip' && \
    mkdir /root/.fonts && \
    unzip 'noto-sans-jp.zip' -d /root/.fonts && \
    fc-cache -fv
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN mkdir /hashtagapp-back
WORKDIR /hashtagapp-back
COPY pyproject.toml poetry.lock /hashtagapp-back/
RUN . $HOME/.poetry/env && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY . /hashtagapp-back
CMD [ "sh", "start.sh" ]
