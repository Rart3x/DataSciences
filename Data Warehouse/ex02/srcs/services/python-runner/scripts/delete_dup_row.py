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

#Delete duplicate rows
delete_query = """
    DELETE FROM customers
    WHERE id NOT IN (
        SELECT id
        FROM (
            SELECT id, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY id) AS rnum
            FROM customers
        ) t
        WHERE t.rnum = 1
    );
"""
cursor.execute(delete_query)

# Close connections
cursor.close()
conn.close()