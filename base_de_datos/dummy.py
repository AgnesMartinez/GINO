
import sqlite3
import pymysql.cursors
from datetime import date, datetime, timedelta
import random
import csv
from docx import Document

output = ""

#conectar a base de datos
DEFAULT_PATH = "./base_de_datos/db.sqlite3"

def db_connect(db_path=DEFAULT_PATH):
    conn = sqlite3.connect(db_path)
    return conn

conn_local = db_connect()

def maria_connect():
    try:
        conn = pymysql.connect(
            user="root",
            password="pruebas",
            host="localhost",
            database="hmi",
            port=3306
        )
        
        return conn

    except Exception as e:
        print(f"Error connecting to MariaDB Platform: {e}")

        
'''
with conn_local:

    cur =  conn_local.cursor()

    query = """SELECT ID,paciente_id,CURP,CUPI,clave,fecha,hora,servicio
               FROM pediatria
               WHERE fecha BETWEEN '2020-07-01' AND '2020-07-30'
               ORDER BY fecha"""

    lista = cur.execute(query)

    for item in lista:
        print(f'-------\n {item}\n')



with open('./base_de_datos/dump.sql', 'w') as f:
    for line in conn_local.iterdump():
        f.write(f'{line}\n')

conn_local.close()
'''















