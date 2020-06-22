FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /cider-map

WORKDIR /cider-map

ADD . /cider-map/

RUN pip install -r requirements.txt
