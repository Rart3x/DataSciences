FROM python:latest

RUN pip install --upgrade pip
RUN pip install psycopg2-binary python-dateutil colorama

WORKDIR /work

RUN mkdir -p /work/scripts/customers

COPY services/python-runner/scripts/*.py /work/scripts/
COPY customer/*.csv /work/scripts/customers/

CMD ["python", "./scripts/automatic_table.py"]