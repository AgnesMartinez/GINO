import PySimpleGUI as sg
import sqlite3
from datetime import date
import concurrent.futures
import pymysql.cursors

#conectar a base de datos local
DEFAULT_PATH = "./base_de_datos/db.sqlite3"

def db_connect(db_path=DEFAULT_PATH):
    conn_local = sqlite3.connect(db_path)
    return conn_local

conn_local = db_connect()

#conectar a base de datos maria
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
        sg.SystemTray.notify('¡Error de conexion en Maria!',f'{e}',display_duration_in_ms=50)

#variables a utilizar
fechahoy = date.today()
output = "" 
catalogo = {}
mcombo = []
mod_query = {}

with conn_local:
    query = """SELECT clave,nombre FROM catalogoinsumos ORDER BY nombre"""
    lista = conn_local.execute(query)
    for item in lista:
        catalogo[item[1]] = item[0]
        mcombo.append(item[1])


def u_300_gine():
    global output

    if values['-BD-'] == 'BD Local':
        query = """SELECT * FROM ginecologia ORDER BY ID DESC LIMIT 300"""

        with conn_local:
            lista = conn_local.execute(query)
            for item in lista:
                output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  Clave: {str(item[3])}  |  Fecha: {str(item[4])}  |  Hora: {str(item[5])}  |  Servicio: {str(item[6])}\n'

    elif values['-BD-'] == 'BD Maria':
        try:
            query = """SELECT * FROM ginecologia ORDER BY ID DESC LIMIT 300"""
            conn_maria = maria_connect()
    
            with conn_maria.cursor() as cursor:
        
                cursor.execute(query)

                lista = cursor.fetchall()
        
                for item in lista:
                    output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  Clave: {str(item[3])}  |  Fecha: {str(item[4])}  |  Hora: {str(item[5])}  |  Servicio: {str(item[6])}\n'
        except:
            pass
    
    else:
        sg.popup('¿CAW?','Selecciona una base de datos!\n')


def u_300_pedia():
    global output

    if values['-BD-'] == 'BD Local':
        query = """SELECT * FROM pediatria ORDER BY ID DESC LIMIT 300"""

        with conn_local:
            lista = conn_local.execute(query)
            for item in lista:
                output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  CUPI: {str(item[3])} | Clave: {str(item[4])}  |  Fecha: {str(item[5])}  |  Hora: {str(item[6])}  |  Servicio: {str(item[7])}\n'

    elif values['-BD-'] == 'BD Maria':
        try:
            query = """SELECT * FROM pediatria ORDER BY ID DESC LIMIT 300"""
            
            conn_maria = maria_connect()
            
            with conn_maria.cursor() as cursor:

                cursor.execute(query)

                lista = cursor.fetchall()

                for item in lista:
                    output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  CUPI: {str(item[3])} | Clave: {str(item[4])}  |  Fecha: {str(item[5])}  |  Hora: {str(item[6])}  |  Servicio: {str(item[7])}\n'
        except:
            pass
    
    else:
        sg.popup('¿CAW?','Selecciona una base de datos!\n')

def borrar_registro_gine():
    if values['-BD-'] == 'BD Local':
        query = """DELETE FROM ginecologia WHERE ID=?"""

        with conn_local:
            conn_local.execute(query,(values['-ID-'],))
    
    elif values['-BD-'] == 'BD Maria':
        try:
            query = """DELETE FROM ginecologia WHERE ID=%s"""
            
            conn_maria = maria_connect()

            with conn_maria.cursor() as cursor:
                cursor.execute(query,(values['-ID-'],))

            conn_maria.commit()

        except:
            pass
    
    else:
        sg.popup('¿CAW?','Selecciona una base de datos!\n')


def borrar_registro_pedia():
    if values['-BD-'] == 'BD Local':
        query = """DELETE FROM pediatria WHERE ID=?"""

        with conn_local:
            conn_local.execute(query,(values['-ID-'],))

    elif values['-BD-'] == 'BD Maria':
        try:
            query = """DELETE FROM pediatria WHERE ID=%s"""

            conn_maria = maria_connect()

            with conn_maria.cursor() as cursor:
                cursor.execute(query,(values['-ID-'],))

            conn_maria.commit()

        except:
            pass
    
    else:
        sg.popup('¿CAW?','Selecciona una base de datos!\n')

def modificar_registro_gine():
    
    mod_query['nombre'] = values['-param1-']
    mod_query['CURP'] = values['-param2-']
    mod_query['servicio'] = values['-param3-']
    mod_query['insumo'] = values['-param4-']

    for key,value in mod_query.items():
        if key == 'nombre' and value:
            if values['-BD-'] == 'BD Local':
                query = """UPDATE ginecologia SET paciente_id=? WHERE ID=?"""
                valores = (values['-nom2-'].upper().strip(),int(values['-ID-']))

                with conn_local:
                    conn_local.execute(query,valores)

            elif values['-BD-'] == 'BD Maria':
                try:
                    query = """UPDATE ginecologia SET paciente_id=%s WHERE ID=%s"""
                    valores = (values['-nom2-'].upper().strip(),int(values['-ID-']))

                    conn_maria = maria_connect()

                    with conn_maria.cursor() as cursor:
                        cursor.execute(query,valores)
                    
                    conn_maria.commit()

                except:
                    pass
            else:
                sg.popup('¿CAW?','Selecciona una base de datos!\n')

        elif key == 'CURP' and value and len(values['-curp2-']) == 18:
            if values['-BD-'] == 'BD Local':
                query = """UPDATE ginecologia SET CURP=? WHERE ID=?"""
                valores = (values['-curp2-'].upper().strip(),int(values['-ID-']))

                with conn_local:
                    conn_local.execute(query,valores)

            elif values['-BD-'] == 'BD Maria':
                try:
                    query = """UPDATE ginecologia SET CURP=%s WHERE ID=%s"""
                    valores = (values['-curp2-'].upper().strip(),int(values['-ID-']))

                    conn_maria = maria_connect()

                    with conn_maria.cursor() as cursor:
                        cursor.execute(query,valores)
                    
                    conn_maria.commit()

                except:
                    pass
            
            else:
                sg.popup('¿CAW?','Selecciona una base de datos!\n')
        
        elif key == 'servicio' and value:
            if values['-BD-'] == 'BD Local':
                query = """UPDATE ginecologia SET servicio=? WHERE ID=?"""
                valores = (values['-servicio-'],int(values['-ID-']))

                with conn_local:
                    conn_local.execute(query,valores)

            elif values['-BD-'] == 'BD Maria':
                try:
                    query = """UPDATE ginecologia SET servicio=%s WHERE ID=%s"""
                    valores = (values['-servicio-'],int(values['-ID-']))

                    conn_maria = maria_connect()

                    with conn_maria.cursor() as cursor:
                        cursor.execute(query,valores)
                    
                    conn_maria.commit()

                except:
                    pass

            else:
                sg.popup('¿CAW?','Selecciona una base de datos!\n')

        elif key == 'insumo' and value:
            if values['-BD-'] == 'BD Local':
                query = """UPDATE ginecologia SET clave=? WHERE ID=?"""
                seleccion = values['-insumo-']
                valores = (catalogo[seleccion],int(values['-ID-']))

                with conn_local:
                    conn_local.execute(query,valores)
                
            elif values['-BD-'] == 'BD Maria':
                try:
                    query = """UPDATE ginecologia SET clave=%s WHERE ID=%s"""
                    seleccion = values['-insumo-']
                    valores = (catalogo[seleccion],int(values['-ID-']))

                    conn_maria = maria_connect()

                    with conn_maria.cursor() as cursor:
                        cursor.execute(query,valores)
                    
                    conn_maria.commit()

                except:
                    pass
            
            else:
                sg.popup('¿CAW?','Selecciona una base de datos!\n')
            

def modificar_registro_pedia():
    
    mod_query['nombre'] = values['-param1-']
    mod_query['CURP'] = values['-param2-']
    mod_query['servicio'] = values['-param3-']
    mod_query['insumo'] = values['-param4-']

    for key,value in mod_query.items():
        if key == 'nombre' and value:
            if values['-BD-'] == 'BD Local':
                query = """UPDATE pediatria SET paciente_id=?, CUPI=? WHERE ID=?"""
                CUPI = generar_cupi2()
                valores = (values['-nom2-'].upper().strip(),CUPI,int(values['-ID-']))

                with conn_local:
                    conn_local.execute(query,valores)
            
            elif values['-BD-'] == 'BD Maria':
                try:
                    query = """UPDATE pediatria SET paciente_id=%s, CUPI=%s WHERE ID=%s"""
                    CUPI = generar_cupi2()
                    valores = (values['-nom2-'].upper().strip(),CUPI,int(values['-ID-']))

                    conn_maria = maria_connect()

                    with conn_maria.cursor() as cursor:
                        cursor.execute(query,valores)
                    
                    conn_maria.commit()

                except:
                    pass
            
            else:
                sg.popup('¿CAW?','Selecciona una base de datos!\n')

        elif key == 'CURP' and value and len(values['-curp2-']) == 12:
            if values['-BD-'] == 'BD Local':
                query = """UPDATE pediatria SET CURP=? WHERE ID=?"""
                valores = (values['-curp2-'].upper().strip(),int(values['-ID-']))

                with conn_local:
                    conn_local.execute(query,valores)
            
            elif values['-BD-'] == 'BD Maria':
                try:
                    query = """UPDATE pediatria SET CURP=%s WHERE ID=%s"""
                    valores = (values['-curp2-'].upper().strip(),int(values['-ID-']))
                    
                    conn_maria = maria_connect()

                    with conn_maria.cursor() as cursor:
                        cursor.execute(query,valores)
                    
                    conn_maria.commit()
                
                except:
                    pass
            
            else:
                sg.popup('¿CAW?','Selecciona una base de datos!\n')

        
        elif key == 'servicio' and value:
            if values['-BD-'] == 'BD Local':
                query = """UPDATE pediatria SET servicio=? WHERE ID=?"""
                valores = (values['-servicio-'],int(values['-ID-']))

                with conn_local:
                    conn_local.execute(query,valores)

            elif values['-BD-'] == 'BD Maria':
                try:
                    query = """UPDATE pediatria SET servicio=%s WHERE ID=%s"""
                    valores = (values['-servicio-'],int(values['-ID-']))

                    conn_maria = maria_connect()

                    with conn_maria.cursor() as cursor:
                        cursor.execute(query,valores)
                    
                    conn_maria.commit()

                except:
                    pass
            
            else:
                sg.popup('¿CAW?','Selecciona una base de datos!\n')
                

        elif key == 'insumo' and value:
            if values['-BD-'] == 'BD Local':
                query = """UPDATE pediatria SET clave=? WHERE ID=?"""
                seleccion = values['-insumo-']
                valores = (catalogo[seleccion],int(values['-ID-']))

                with conn_local:
                    conn_local.execute(query,valores)
            
            elif values['-BD-'] == 'BD Maria':
                try:
                    query = """UPDATE pediatria SET clave=%s WHERE ID=%s"""
                    seleccion = values['-insumo-']
                    valores = (catalogo[seleccion],int(values['-ID-']))

                    conn_maria = maria_connect()

                    with conn_maria.cursor() as cursor:
                        cursor.execute(query,valores)
                    
                    conn_maria.commit()
                
                except:
                    pass
            
            else:
                sg.popup('¿CAW?','Selecciona una base de datos!\n')


def busqueda_gine():
    """Funcion para buscar registros en la tabla de ginecologia"""
    global output
    
    if values['-BD-'] == 'BD Local':
        query = """SELECT ginecologia.ID,ginecologia.clave, ginecologia.fecha, ginecologia.hora, ginecologia.servicio, catalogoinsumos.nombre  
        FROM ginecologia,catalogoinsumos 
        WHERE ginecologia.CURP=? 
        AND ginecologia.clave = catalogoinsumos.clave 
        ORDER BY ginecologia.ID DESC"""

        curp = values['-curp-'].upper().strip()
        with conn_local:
            lista = conn_local.execute(query,(curp,))
            for item in lista:
                output += f'--------------------------------\nID: {str(item[0])} | Clave: {str(item[1])} | Fecha: {str(item[2])} | Hora: {str(item[3])} | Servicio: {str(item[4])}\n{str(item[5])}\n'

    elif values['-BD-'] == 'BD Maria':
        try:
            query = """SELECT ginecologia.ID,ginecologia.clave,ginecologia.fecha, ginecologia.hora,ginecologia.servicio,catalogoinsumos.nombre 
            FROM ginecologia,catalogoinsumos 
            WHERE ginecologia.CURP=%s 
            AND ginecologia.clave = catalogoinsumos.clave 
            ORDER BY ginecologia.ID DESC LIMIT 35"""

            curp = values['-curp-'].upper().strip()
        
            conn_maria = maria_connect()

            with conn_maria.cursor() as cursor:
                cursor.execute(query,(curp,))

                lista = cursor.fetchall()
        
                for item in lista:
                    output += f'--------------------------------\nID: {str(item[0])} | Clave: {str(item[1])} | Fecha: {str(item[2])} | Hora: {str(item[3])} | Servicio: {str(item[4])}\n{str(item[5])}\n'
        
        except:
            pass
    
    else:
        sg.popup('¿CAW?','Selecciona una base de datos!\n')


def busqueda_pedia():
    """Funcion para buscar registros en tabla de pediatria"""
    global output

    if values['-BD-'] == 'BD Local':
        query = """SELECT pediatria.ID,pediatria.clave,pediatria.fecha,pediatria.hora, pediatria.servicio, catalogoinsumos.nombre 
        FROM pediatria,catalogoinsumos 
        WHERE pediatria.paciente_id=?
        AND pediatria.CUPI=? 
        AND pediatria.clave = catalogoinsumos.clave 
        ORDER BY pediatria.ID DESC"""

        nombre = values['-nombre-'].upper().strip()
        CUPI = generar_cupi()

        with conn_local:
            lista = conn_local.execute(query,(nombre,CUPI))
            for item in lista:
                output += f'--------------------------------\nID: {str(item[0])} | Clave: {str(item[1])} | Fecha: {str(item[2])} | Hora: {str(item[3])} | Servicio: {str(item[4])}\n{str(item[5])}\n'

    elif values['-BD-'] == 'BD Maria':

        try:
            query = """SELECT pediatria.ID,pediatria.clave,pediatria.fecha,pediatria.hora,pediatria.servicio,catalogoinsumos.nombre 
            FROM pediatria,catalogoinsumos 
            WHERE pediatria.paciente_id=%s
            AND pediatria.CUPI=%s
            AND pediatria.clave = catalogoinsumos.clave 
            ORDER BY pediatria.ID DESC LIMIT 35"""

            nombre = values['-nombre-'].upper().strip()
            CUPI = generar_cupi()

            conn_maria = maria_connect()

            with conn_maria.cursor() as cursor:
                cursor.execute(query,(nombre,CUPI))

                lista = cursor.fetchall()

                for item in lista:
                    output += f'--------------------------------\nID: {str(item[0])} | Clave: {str(item[1])} | Fecha: {str(item[2])} | Hora: {str(item[3])} | Servicio: {str(item[4])}\n{str(item[5])}\n'

        except:
            pass
    
    else:
        sg.popup('¿CAW?','Selecciona una base de datos!\n')


def busqueda_pclave_gine():
    """Busqueda por palabras clave ginecologia"""

    global output

    input_usuario = values['-nombre-'].upper().strip()

    if input_usuario != "" and len(input_usuario) > 2:
        valor = f'%{input_usuario}%'

        if values['-BD-'] == 'BD Local':
            query="""SELECT * FROM ginecologia WHERE paciente_id LIKE ? ORDER BY ID DESC"""
                
            with conn_local:
                lista = conn_local.execute(query,(valor,))

                for item in lista:
                    output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  Clave: {str(item[3])}  |  Fecha: {str(item[4])}  |  Hora: {str(item[5])}  |  Servicio: {str(item[6])}\n'

        elif values['-BD-'] == 'BD Maria':
            try:
                query="""SELECT * FROM ginecologia WHERE paciente_id LIKE %s ORDER BY ID DESC"""

                conn_maria = maria_connect()    
            
                with conn_maria.cursor() as cursor:
                    lista = cursor.execute(query,(valor,))

                    for item in lista:
                        output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  Clave: {str(item[3])}  |  Fecha: {str(item[4])}  |  Hora: {str(item[5])}  |  Servicio: {str(item[6])}\n'
            except:
                pass

        else:
            sg.popup('¿CAW?','Selecciona una base de datos!\n')

    else:
        sg.popup('¿CAW?','Necesitas ingresar al menos 3 letras para iniciar la busqueda!\n')


def busqueda_pclave_pedia():
    """Busqueda por palabras clave en BD Maria"""
    global output

    input_usuario = values['-nombre-'].upper().strip()

    if input_usuario != "" and len(input_usuario) > 2:
        valor = f'%{input_usuario}%'    
        
        if values['-BD-'] == 'BD Local':

            query="""SELECT * FROM pediatria WHERE paciente_id LIKE ? ORDER BY ID DESC"""
                
            with conn_local:
                lista = conn_local.execute(query,(valor,))

                for item in lista:
                    output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  CUPI: {str(item[3])} | Clave: {str(item[4])}  |  Fecha: {str(item[5])}  |  Hora: {str(item[6])}  |  Servicio: {str(item[7])}\n'
    
        elif values['-BD-'] == 'BD Maria':
            try:
                query="""SELECT * FROM pediatria WHERE paciente_id LIKE %s ORDER BY ID DESC"""
                
                conn_maria = maria_connect()

                with conn_maria.cursor() as cursor:
                    lista = cursor.execute(query,(valor,))

                    for item in lista:
                        output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  CUPI: {str(item[3])} | Clave: {str(item[4])}  |  Fecha: {str(item[5])}  |  Hora: {str(item[6])}  |  Servicio: {str(item[7])}\n'
            
            except:
                pass

        else:
            sg.popup('¿CAW?','Selecciona una especialidad!\n')

    else:
        sg.popup('¿CAW?','Necesitas ingresar al menos 3 letras para continuar la busqueda!\n')


def busqueda_fecha_gine():
    """Busqueda por fecha en ginecologia"""

    global output

    input_usuario = values['-fechab-'].replace("/","-")
        
    if input_usuario != "":
        
        if values['-BD-'] == 'BD Local':

            query="""SELECT * FROM ginecologia WHERE fecha= ? ORDER BY ID DESC"""
                
            with conn_local:
                lista = conn_local.execute(query,(input_usuario,))

                for item in lista:
                    output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  Clave: {str(item[3])}  |  Fecha: {str(item[4])}  |  Hora: {str(item[5])}  |  Servicio: {str(item[6])}\n'

        elif values['-BD-'] == 'BD Maria':
            
            try:
                query="""SELECT * FROM ginecologia WHERE fecha = %s ORDER BY ID DESC"""
                
                conn_maria = maria_connect()

                with conn_maria.cursor() as cursor:
                    cursor.execute(query,(input_usuario,))

                    lista = cursor.fetchall()

                    for item in lista:
                        output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  Clave: {str(item[3])}  |  Fecha: {str(item[4])}  |  Hora: {str(item[5])}  |  Servicio: {str(item[6])}\n'
            except:
                pass
            
        else:
            sg.popup('¿CAW?','Selecciona una base de datos!\n')

    else:
        sg.popup('¿CAW?','Necesitas ingresar una fecha!\n')

def busqueda_fecha_pedia():
    """Busqueda por fecha en pediatria"""

    global output
    input_usuario = values['-fechab-'].replace('/','-')
        
    if input_usuario != "":
        
        if values['-BD-'] == 'BD Local':

            query="""SELECT * FROM pediatria WHERE fecha= ? ORDER BY ID DESC"""
             
            with conn_local:
                lista = conn_local.execute(query,(input_usuario,))

                for item in lista:
                        output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  CUPI: {str(item[3])} | Clave: {str(item[4])}  |  Fecha: {str(item[5])}  |  Hora: {str(item[6])}  |  Servicio: {str(item[7])}\n'

        elif values['-BD-'] == 'BD Maria':
            try:
                query="""SELECT * FROM pediatria WHERE fecha = %s ORDER BY ID DESC"""

                conn_maria = maria_connect()    
            
                with conn_maria.cursor() as cursor:
                    cursor.execute(query,(input_usuario,))

                    lista = cursor.fetchall()

                    for item in lista:
                        output += f'--------------------------------\nID: {str(item[0])}  |  Nombre: {str(item[1])}  |  CURP: {str(item[2])}  |  CUPI: {str(item[3])} | Clave: {str(item[4])}  |  Fecha: {str(item[5])}  |  Hora: {str(item[6])}  |  Servicio: {str(item[7])}\n'
            except:
                pass
        
        else:
            sg.popup('¿CAW?','Selecciona una base de datos!\n')

    else:
        sg.popup('¿CAW?','Necesitas ingresar una fecha!\n')


def generar_cupi():
    """Funcion para generar el CUPI (Clave Unica Pediatrica de Identificacion)"""
    apellidos = values['-nombre-'].upper().strip().replace('RN','').split()
    fn = values['-fn-'].replace('/','')
    if values['-masc-']:
        sexo = "H"
    elif values['-fem-']:
        sexo = "M"
    CUPI = f'{apellidos[0][0:2]}{apellidos[1][0:2]}{fn[2:]}{sexo}'
    return CUPI


def generar_cupi2():
    """Funcion para generar el CUPI (Clave Unica Pediatrica de Identificacion)"""
    apellidos = values['-nom2-'].upper().strip().replace('RN','').split()
    fn = values['-fn2-'].replace('/','')
    if values['-masc2-']:
        sexo = "H"
    elif values['-fem2-']:
        sexo = "M"
    CUPI = f'{apellidos[0][0:2]}{apellidos[1][0:2]}{fn[2:]}{sexo}'
    return CUPI

def sincronizar_maria():
    """Funcion para sincronizar registros de BD local con BD maria"""
    #Ambos servicios al mismo tiempo
    try:
        with conn_local:

            cur = conn_local.cursor()

            query = """SELECT paciente_id,CURP,CUPI,clave,fecha,hora,servicio FROM pediatria WHERE synced=0"""

            cur.execute(query)

            lista_pedia = cur.fetchall()

            conn_maria = maria_connect()

            with conn_maria.cursor() as cursor:
                query = """INSERT INTO pediatria (paciente_id,CURP,CUPI,clave,fecha,hora,servicio) VALUES (%s,%s,%s,%s,%s,%s,%s)"""

                cursor.executemany(query,lista_pedia)

                conn_maria.commit()

            query2 = """SELECT paciente_id,CURP,clave,fecha,hora,servicio FROM ginecologia WHERE synced=0"""

            cur.execute(query2)

            lista_gine =  cur.fetchall()

            with conn_maria.cursor() as cursor:    

                query = """INSERT INTO ginecologia (paciente_id,CURP,clave,fecha,hora,servicio) VALUES (%s,%s,%s,%s,%s,%s)"""
    
                cursor.executemany(query,lista_gine)

                conn_maria.commit()

            query3 = """SELECT ID FROM pediatria WHERE synced=0"""

            cur.execute(query3)

            sync_pedia =  cur.fetchall()

            query4 = """UPDATE pediatria SET synced = 1 WHERE ID = ?"""

            cur.executemany(query4,sync_pedia)
        
            query5 = """SELECT ID FROM ginecologia WHERE synced=0"""

            cur.execute(query5)

            sync_gine = cur.fetchall()

            query6 = """UPDATE ginecologia SET synced = 1 WHERE ID = ?"""

            cur.executemany(query6,sync_gine)
    
    except:
        pass


#Interfaz Grafica - PySimpleGUI
sg.theme('Teal Mono')  # Colores!

#Elementos en ventana         

Info_Paciente = [
    [sg.Text('Nombre del paciente'), sg.Input(size=(45,2), key='-nombre-'), sg.Text('CURP'), sg.Input(size=(20,2), key='-curp-')],
    [sg.Text('(Solo Pediatria)'),sg.CalendarButton('Fecha de Nacimiento', target=(1,2), auto_size_button=True, format='%Y/%m/%d'), 
     sg.Input(size=(13,2), key='-fn-'), sg.Radio('Masculino', "RADIO1",key='-masc-'), sg.Radio('Femenino', "RADIO1",default=True, key='-fem-')],
    [sg.Text('Especialidad'),sg.Combo(['Ginecologia y Obstetricia', 'Pediatria'], size=(25,2), readonly=True, key='-esp-'), sg.Text('Base de Datos'),
     sg.Combo(['BD Local', 'BD Maria'], size=(15,2), readonly=True, key='-BD-'), sg.Text('   '), sg.Button('Buscar Registros')]
]

AreaHerramientas = [
    [sg.Button('Ultimos registros por especialidad'),sg.Button('Busqueda por palabras clave')],
    [sg.CalendarButton('Calendario', target=(1,1), auto_size_button=True, format='%Y/%m/%d'),
     sg.Input(size=(13,2), key='-fechab-'),sg.Button('Busqueda por fecha')],
    [sg.Button('Exportar Base de Datos')]
]

AreaRegistros = [
    [sg.Multiline(size=(162,20),disabled=True,key='-output-')]
]

AreaCambios = [
    [sg.Text('ID'),sg.Input(size=(6,2), key='-ID-'), sg.Checkbox(' Nombre',key='-param1-'), sg.Input(size=(30,2), key='-nom2-'),
    sg.Checkbox(' CURP', key='-param2-'), sg.Input(size=(20,2), key='-curp2-'), sg.Checkbox('Servicio', key='-param3-'), sg.Combo(['Urgencias GyO',
    'Labor / Toco (GyO)','Quirofano GyO','Alojamiento Conjunto GyO','Modulo Mater','Urgencias Pediatria',
    'Labor / Toco (Pediatria)', 'Quirofano Pediatria','UCIN','Cunero Patologico','Cuidados Intermedios',
    'Alojamiento Conjunto Pediatria'], size=(35,12), readonly=True, key='-servicio-')],
    [sg.Text('(Solo Pediatria)'),sg.CalendarButton('Fecha de Nacimiento', target=(1,2), auto_size_button=True, format='%Y/%m/%d'), 
     sg.Input(size=(13,2), key='-fn2-'), sg.Radio('Masculino', "RADIO2",key='-masc2-'), sg.Radio('Femenino', "RADIO2",default=True, key='-fem2-')],
    [sg.Checkbox(' Insumo', key='-param4-'), sg.Combo(mcombo, size=(90,6), key='-insumo-'),sg.Button('Modificar Registro'), sg.Button('Borrar Registro')]
]


# Acomodo de elementos de ventana
layout = [
    [sg.Frame('Busqueda por paciente', Info_Paciente), sg.Frame('Herramientas', AreaHerramientas)],
    [sg.Frame('Consulta de registros', AreaRegistros)],
    [sg.Frame('Modificar registros', AreaCambios)]
]

#Ventana
window = sg.Window('HMI - Explorador Base De Datos', layout)

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.submit(sincronizar_maria())

#Parte funcional de la aplicacion

while True:  # Mantenerla persistente
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break
    
    #Herramientas del explorador
    #Ultimos 300 registros
    elif event == 'Ultimos registros por especialidad':
        if values['-esp-'] == 'Ginecologia y Obstetricia':
            u_300_gine()
            window['-output-'].update(output)
            output = ""
        
        elif values['-esp-'] == 'Pediatria':
            u_300_pedia()
            window['-output-'].update(output)
            output = ""
            
        else:
            sg.popup('¿CAW?','Selecciona una especialidad!\n')
    
    #Busqueda por palabras clave
    elif event == 'Busqueda por palabras clave':
        if values['-esp-'] == 'Ginecologia y Obstetricia':
            busqueda_pclave_gine()
            window['-output-'].update(output)
            output = ""

        elif values['-esp-'] == 'Pediatria':
            busqueda_pclave_pedia()
            window['-output-'].update(output)
            output = ""
        
        else:
            sg.popup('¿CAW?','Selecciona una especialidad!\n')

    #Busqueda por fecha
    elif event == 'Busqueda por fecha':
        if values['-esp-'] == 'Ginecologia y Obstetricia':
            busqueda_fecha_gine()
            window['-output-'].update(output)
            output = ""

        elif values['-esp-'] == 'Pediatria':
            busqueda_fecha_pedia()
            window['-output-'].update(output)
            output = ""
        
        else:
            sg.popup('¿CAW?','Selecciona una especialidad!\n')
        
    
    #Modificar registros
    elif event == 'Modificar Registro':
        if values['-ID-'].isdigit() and values['-ID-'] != "":
            if values['-esp-'] == 'Ginecologia y Obstetricia':
                modificar_registro_gine()
                
                if values['-curp-'] != "": 
                    busqueda_gine()
                    window['-output-'].update(output)
                    output = ""
                        
                elif values['-curp-'] == "":
                    u_300_gine()
                    window['-output-'].update(output)
                    output = ""

            elif values['-esp-'] == 'Pediatria':    
                modificar_registro_pedia()
                
                if values['-nombre-'] != "": 
                    busqueda_pedia()
                    window['-output-'].update(output)
                    output = ""
                    
                elif values['-nombre-'] == "":
                    u_300_pedia()
                    window['-output-'].update(output)
                    output = ""

            else:
                sg.popup('CAW','No olvides seleccionar una especialidad!\n')
        else:
            sg.popup('CAW','El ID del registro es el elemento mas importante!\n\nAsegurate de que sea el correcto (¡y que sea un numero!)\n')

    #Borrar Registros
    elif event == 'Borrar Registro':
        if values['-ID-'].isdigit() and values['-ID-'] != "":
            if values['-esp-'] == 'Ginecologia y Obstetricia':
                answer = sg.popup_yes_no('¿Estas seguro que desea borrar el registro?')
                if answer == 'Yes':
                    borrar_registro_gine()
                    if values['-curp-'] != "": 
                        busqueda_gine()
                        window['-output-'].update(output)
                        output = ""
                        
                    elif values['-curp-'] == "":
                        u_300_gine()
                        window['-output-'].update(output)
                        output = ""

            elif values['-esp-'] == 'Pediatria':
                answer = sg.popup_yes_no('¿Estas seguro que desea borrar el registro?')
                if answer == 'Yes':
                    borrar_registro_pedia()
                    if values['-nombre-'] != "": 
                        busqueda_pedia()
                        window['-output-'].update(output)
                        output = ""
                        
                    elif values['-nombre-'] == "":
                        u_300_pedia()
                        window['-output-'].update(output)
                        output = ""
            else:
                sg.popup('¿CAW?','No olvides seleccionar una especialidad!\n')
        else:
            sg.popup('CAW','El ID del registro es el elemento mas importante!\n\nAsegurate de que sea el correcto (¡y que sea un numero!)')
        
    #Buscar Registros
    elif event == 'Buscar Registros':
        if values['-esp-'] == 'Ginecologia y Obstetricia':
            if values['-nombre-'] != '' and values['-curp-'] != '':
                busqueda_gine()
                window['-output-'].update(output)
                output = ""
            
            else:
                sg.popup('¿CAW?','No olvides los datos del paciente! (Nombre y CURP)\n')
   
        elif values['-esp-'] == 'Pediatria':
            if values['-nombre-'] != '' and len(values['-fn-']) == 10:
                busqueda_pedia()
                window['-output-'].update(output)
                output = ""

            else:
                sg.popup('¿CAW?','No olvides los datos del paciente! (Nombre y Fecha Nacimiento)\n')

        else:
            sg.popup('¿CAW?','No olvides seleccionar un servicio!\n')

window.close()