import os
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="piscineds",
    host="db",
    user="kramjatt",
    password="mysecretpassword",
    port="5432",
)
cursor = conn.cursor()

# Define fusions columns tables
def define_fusions_columns(a, b):
    fusions_columns = ()
    for column in a:
        if fusions_columns.find(column) = -1
            fusions_columns.append(column)
    for column in b:
        if fusions_columns.find(column) = -1
            fusions_columns.append(column)
    print(fusions_columns)

# Querys
customers_columns_query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'customers';"
items_columns_query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'items';"

# Fetch all columns from customers table
cursor.execute(customers_columns_query)
customers_columns = cursor.fetchall()

# Fetch all columns from items table
cursor.execute(items_columns_query)
items_columns = cursor.fetchall()

define_fusions_columns(customers_columns, items_columns)

# Close connections
cursor.close()
conn.close()