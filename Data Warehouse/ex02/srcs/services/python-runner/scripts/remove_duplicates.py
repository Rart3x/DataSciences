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
    return f"SELECT COUNT(*) AS occurencies, {column_definitions} FROM customers GROUP BY {column_definitions} HAVING COUNT(*) > 1;"

# Querys
columns_query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'customers';"

# Fetch all columns from customers table
cursor.execute(columns_query)
columns = cursor.fetchall()

print(define_occurencies_q(columns))

# Close connections
cursor.close()
conn.close()