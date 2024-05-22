FROM python:3.10-alpine

RUN apk update && apk upgrade
RUN apk add --no-cache gcc g++ build-base wget

USER root
RUN adduser -D celery
RUN addgroup celery celery
RUN addgroup root celery

RUN pip install --upgrade pip

WORKDIR /app
COPY ./ ./

COPY ./requirements.txt /.
RUN pip install -r requirements.txt

COPY ./docker/celery/celeryd /etc/init.d/
COPY ./docker/celery/celerybeat /etc/init.d/
COPY ./docker/celery/config/celeryd /etc/default/
RUN ["chmod", "755", "/etc/init.d/celeryd"]
RUN ["chmod", "755", "/etc/init.d/celerybeat"]
RUN ["chmod", "640", "/etc/default/celeryd"]

RUN ["chmod", "+x", "docker/celery-worker/entry.sh"]
ENTRYPOINT ["docker/celery-worker/entry.sh"]