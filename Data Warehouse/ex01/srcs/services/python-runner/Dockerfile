FROM python:latest

RUN pip install --upgrade pip
RUN pip install psycopg2-binary python-dateutil colorama

WORKDIR /work

RUN mkdir -p /work/scripts/customers

COPY customer/*.csv /work/scripts/customers/
COPY services/python-runner/scripts/*.py /work/scripts/
COPY services/python-runner/scripts/*.sh /work/scripts/

CMD ["/bin/bash", "/work/scripts/scripts.sh"]