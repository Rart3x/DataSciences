FROM python:latest

RUN pip install --upgrade pip
RUN pip install psycopg2-binary python-dateutil colorama

WORKDIR /work

COPY services/python-runner/scripts/*.py /work/scripts/
COPY services/python-runner/scripts/*.sh /work/scripts/

CMD ["/bin/bash", "/work/scripts/scripts.sh"]