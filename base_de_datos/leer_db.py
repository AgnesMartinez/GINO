
import sqlite3
import pymysql.cursors



#conectar a base de datos local
DEFAULT_PATH = "./base_de_datos/db.sqlite3"

def db_connect(db_path=DEFAULT_PATH):
    conn_local = sqlite3.connect(db_path)
    return conn_local

conn_local = db_connect()

#iniciar cursor para querys
cur = conn_local.cursor()

query = """SELECT * FROM ginecologia"""

cur.execute(query)

lista = cur.fetchall()

for item in lista:
    print(f'===========\n {item}')



'''

#Leer a maria
def maria_connect():
    try:
        conn = pymysql.connect(
            user="agnesm",
            password="torrente",
            host="192.168.1.11",
            database="hmi",
            port=3307
        )
        
        return conn

    except Exception as e:
        print(f'Error connecting to MariaDB Platform: {e} ')

conn_maria = maria_connect()

with conn_maria.cursor() as cursor:

    query2 = """SELECT * FROM pediatria"""
    cursor.execute(query2)
    
    for item in cursor.fetchall():
        print(f'===========\n {item}')

'''