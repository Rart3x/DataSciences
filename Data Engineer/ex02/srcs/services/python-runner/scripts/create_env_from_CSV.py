import os, psycopg2

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

file_content = []
py_files_content = []

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        table_name = filename[:-4]
        with open(os.path.join(directory, filename), 'r') as file:
            file_content = file.readlines()
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY)"
            cursor.execute(query)
            conn.commit()  
        py_files_content.append(file_content)

cursor.close()
conn.close()