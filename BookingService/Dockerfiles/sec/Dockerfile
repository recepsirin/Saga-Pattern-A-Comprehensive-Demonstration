FROM python:3

MAINTAINER Recep Sirin

COPY ../../requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ../../ app


CMD python sec.py