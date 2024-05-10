FROM python:latest

RUN pip install --upgrade pip
RUN pip install psycopg2-binary python-dateutil colorama

WORKDIR /work

RUN mkdir -p /work/scripts/customers
RUN mkdir -p /work/scripts/items

COPY services/python-runner/scripts/*.py /work/scripts/
COPY customer/*.csv /work/scripts/customers/
COPY items/*.csv /work/scripts/items/

CMD ["python", "./scripts/items_table.py"]