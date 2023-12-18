import os, psycopg2
from dateutil import parser

conn = psycopg2.connect(
    dbname="piscineds",
    host="localhost",
    user="kramjatt",
    password="mysecretpassword",
    port="5432",
)
cursor = conn.cursor()

# directory = './customers/'
directory = '../../db/customer/'

def create_fields(table_name, types_dict):
    for key in types_dict:
        alter_query = f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS "{key}" {types_dict[key]}'
        cursor.execute(alter_query)
        conn.commit()

def create_tables(table_name):
    create_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY)"
    cursor.execute(create_query)
    conn.commit()

def define_type(field):
    try:
        if field.lower() == "true" or field.lower() == "false":
            return "BOOLEAN"
    
        int(field)
        return "INTEGER"

    except ValueError:
        try:
            parser.parse(field)
            return "DATE"

        except ValueError:
            return "VARCHAR(255)"

def insert_data(table_name, fields, file_content):
    for line in file_content[1:]:
        values = line.split(',')
        formatted_values = [f"'{value.strip()}'" for value in values]
        insert_query = f'INSERT INTO {table_name} ({", ".join(fields)}) VALUES ({", ".join(formatted_values)})'
        cursor.execute(insert_query)
        conn.commit()

def fill_types_dict(fields, table_name, types):
    types_dict = {}
    for i in range(len(fields)):
        types_dict[fields[i].strip()] = define_type(types[i].strip())
    create_fields(table_name, types_dict)

fields = []
file_content = []
py_files_content = []

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        table_name = filename[:-4]
        create_tables(table_name)
        with open(os.path.join(directory, filename), 'r') as file:
            file_content = file.readlines()
            if file_content.__len__() > 1:
                fields = file_content[0].split(',')
                types = file_content[1].split(',')
                fill_types_dict(fields, table_name, types)
                insert_data(table_name, fields, file_content)

cursor.close()
conn.close()
