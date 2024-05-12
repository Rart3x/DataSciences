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

idx = 0

#Delete duplicate rows
query = "SELECT * FROM customers"

cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close connections
cursor.close()
conn.close()