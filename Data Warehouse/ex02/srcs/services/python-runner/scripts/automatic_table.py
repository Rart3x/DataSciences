import os
import psycopg2

from datetime import datetime
from colorama import Fore, Style

# Database connection
conn = psycopg2.connect(
    dbname="piscineds",
    host="db",
    user="kramjatt",
    password="mysecretpassword",
    port="5432",
)
cursor = conn.cursor()

# Repository
DIRECTORY = '/work/scripts/customers/'

# Errors
DATE_ERROR = f"{Fore.RED}error: first field must be a date for : {Style.RESET_ALL}"
FIELD_ERROR = f"{Fore.RED}error: fields types must be the same for : {Style.RESET_ALL}"
FIELD_NUMBER_ERROR = f"{Fore.RED}error: number of fields must be the same for : {Style.RESET_ALL}"

# Execute and commit
def executeAndCommit(query):
    cursor.execute(query)
    conn.commit()

# Type define
def defineType(field):
    try:
        if field in ["TRUE", "FALSE", "true", "false"]:
            return "BOOLEAN"
        
        int(field)
        return "BIGINT"

    except ValueError:
        try:
            float(field)
            return "FLOAT"
        
        except ValueError:
            if len(field) == 1:
                return "CHAR"
            try:
                datetime.strptime(field, '%Y-%m-%d %H:%M:%S %Z')
                return "DATE"

            except ValueError:
                try:
                    datetime.strptime(field, '%m/%d/%Y')
                    return "DATE"
                
                except ValueError:
                    return "VARCHAR(255)"

# Tables creations
def createTable(tableName, fields):
    field_definitions = ', '.join([f'"{field}" {fields[field]}' for field in fields])
    create_query = f"CREATE TABLE IF NOT EXISTS {tableName} ({field_definitions})"
    executeAndCommit(create_query)

# Tables inserts
def insertData(tableName, fields, fileContent):
    for line in fileContent[1:]:
        lineTypes = [defineType(value.strip()) for value in line.split(',')]
        if lineTypes != [fields[key] for key in fields]:
            print(FIELD_ERROR + tableName + " at line: " + line)
        else:
            values = line.split(',')
            stripped_values = [f"'{value.strip()}'" for value in values]
            insert_query = f'INSERT INTO {tableName} ({", ".join(fields)}) VALUES ({", ".join(stripped_values)})'
            executeAndCommit(insert_query)

# CSV treatments
for filename in os.listdir(DIRECTORY):
    if filename.endswith('.csv'):
        tableName = filename[:-4]
        with open(os.path.join(DIRECTORY, filename), 'r') as file:
            fileContent = file.readlines()
            if len(fileContent) > 1:
                fields = {field.strip(): defineType(value.strip()) for field, value in zip(fileContent[0].split(','), fileContent[1].split(','))}
                createTable(tableName, fields)
                insertData(tableName, fields, fileContent)

# Close connections
cursor.close()
conn.close()