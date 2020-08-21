
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


#with conn:
#    query = """SELECT * FROM pediatria"""
#    transacciones = conn.execute(query)
#    for item in transacciones:
#        print(f'---------------\n{item}\n')


#lista = []
#i = 0
#with open('./base_de_datos/catalogobkp.csv','r',encoding='utf-8',) as csv_file:
#    csv_reader = csv.reader(csv_file, delimiter=',')
#
#    for row in csv_reader:
#        lista.append([row[0].replace('.','-'),row[1].upper(),row[2].upper()])
#
#
#with open('./base_de_datos/catalogo.csv','w', encoding='utf-8',newline="\n") as csv_file:
#    csv_writer = csv.writer(csv_file, delimiter=',')
#
#    for item in lista:
#        csv_writer.writerow(item)

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












