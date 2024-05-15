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

def define_occurencies_q(columns):
    column_definitions = ', '.join([f'{column[0]}' for column in columns])
    return f"""
        SELECT {column_definitions}
        FROM customers 
        GROUP BY {column_definitions}
        HAVING COUNT(*) > 1;
    """

def del_occurencies_q(columns, occurencies):
    column_definitions = ', '.join([f'{column[0]}' for column in columns])
    return f"""
        WITH CTE AS (
            SELECT ctid, {column_definitions},
                ROW_NUMBER() OVER(PARTITION BY {column_definitions}) AS RN
            FROM customers
        )
        DELETE FROM customers
        WHERE ctid IN (
            SELECT ctid
            FROM CTE
            WHERE RN > 1
        );
    """

# Querys
columns_query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'customers';"

# Fetch all columns from customers table
cursor.execute(columns_query)
columns = cursor.fetchall()

# Fetch all duplicates occurencies from 'customers' table
cursor.execute(define_occurencies_q(columns))
occurencies = cursor.fetchall()

# Delete all duplicates occurencies from 'customers' table
print(del_occurencies_q(columns, occurencies))
cursor.execute(del_occurencies_q(columns, occurencies))

# Close connections
cursor.close()
conn.close()