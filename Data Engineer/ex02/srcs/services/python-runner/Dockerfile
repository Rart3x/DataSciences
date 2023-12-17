FROM python:latest

RUN pip install --upgrade pip
RUN pip install psycopg2-binary

WORKDIR /work

RUN mkdir -p /work/scripts/customers

COPY services/python-runner/scripts/*.py /work/scripts/
COPY services/db/customer/*.csv /work/scripts/customers/

RUN python /work/scripts/create_env_from_CSV.py