import os
import psycopg2
from dateutil import parser
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
FIELD_ERROR = f"{Fore.RED}error: fields must be the same for : {Style.RESET_ALL}"
FIELD_NUMBER_ERROR = f"{Fore.RED}error: number of fields must be the same for : {Style.RESET_ALL}"

# Type define
def defineType(field):
    try:
        if field.lower() in ["true", "false"]:
            return "BOOLEAN"
        
        int(field)
        return "INTEGER"

    except ValueError:
        try:
            parser.parse(field)
            return "DATE"

        except ValueError:
            return "VARCHAR(255)"

# Tables creations
def createTable(tableName, fields):
    field_definitions = ', '.join([f'"{field}" {fields[field]}' for field in fields])
    createQuery = f"CREATE TABLE IF NOT EXISTS {tableName} ({field_definitions})"
    cursor.execute(createQuery)
    conn.commit()

# Tables inserts
def insertData(tableName, fields, fileContent):
    for line in fileContent[1:]:
        lineTypes = [defineType(value.strip()) for value in line.split(',')]
        if lineTypes != [fields[key] for key in fields]:
            print(FIELD_ERROR + tableName + " at line: " + line)
            return
        values = line.split(',')
        strippedValues = [f"'{value.strip()}'" for value in values]
        insert_query = f'INSERT INTO {tableName} ({", ".join(fields)}) VALUES ({", ".join(strippedValues)})'
        cursor.execute(insert_query)
        conn.commit()

# CSV treatments
for filename in os.listdir(DIRECTORY):
    if filename.endswith('.csv'):
        tableName = filename[:-4]
        with open(os.path.join(DIRECTORY, filename), 'r') as file:
            fileContent = file.readlines()
            if len(fileContent) > 1:
                fields = {field.strip(): defineType(value.strip()) for field, value in zip(fileContent[0].split(','), fileContent[1].split(','))}
                if fields[fileContent[0].split(',')[0].strip()] == "DATE":
                    createTable(tableName, fields)
                    insertData(tableName, fields, fileContent)
                else:
                    print(DATE_ERROR + tableName)

# Close connections
cursor.close()
conn.close()