FROM python:3.6.2-alpine3.6
ENV CONFIG_PATH "cfg/main.docker.cfg"
ENV LIBRARY_PATH=/lib:/usr/lib
RUN mkdir /yob-bot/
WORKDIR /yobit-bot
ADD requirements.txt /yobit-bot/
RUN apk add --no-cache build-base jpeg-dev zlib-dev && pip install -r requirements.txt && apk del build-base
ADD . /yobit-bo/
CMD ["python", "-u", "main.py"]