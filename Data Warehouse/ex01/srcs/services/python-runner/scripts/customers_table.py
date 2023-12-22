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

# Get all tables
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
tables = cursor.fetchall()

filtered_tables = [table[0] for table in tables if table[0].startswith('data_202')]

# Merge tables
if filtered_tables:
    merge_query = "CREATE TABLE customers AS SELECT * FROM {};".format(' UNION ALL SELECT * FROM '.join(filtered_tables))
    cursor.execute(merge_query)
    conn.commit()
else:
    print("error: no tables to merge")

# Close connections
cursor.close()
conn.close()