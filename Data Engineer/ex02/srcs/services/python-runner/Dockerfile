FROM python:latest

RUN mkdir /scripts

COPY /scripts/*.py /scripts/

WORKDIR /scripts

RUN "python create_env_from_CSV.py"