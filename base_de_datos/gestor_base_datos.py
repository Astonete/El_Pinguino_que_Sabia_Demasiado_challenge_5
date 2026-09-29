import sqlite3
from typing import List, Dict, Any, Optional

RUTA_BASE_DATOS= "base_de_datos/registros_sistema.db"

def inicializar_base_de_datos()-> None:
    """Crea la tabla 'logs' en la base de datos SQLite si aún no existe.
    """
    conexion_sqlite=sqlite3.connect(RUTA_BASE_DATOS)
    cursor_base_datos=conexion_sqlite.cursor()

    consulta_cracion_tabla="""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT),
        timestamp TEXT NOT NULL,
        servicio TEXT NOT NULL,
        gravedad TEXT NOT NULL,
        mensaje TEXT NOT NULL
        );
    CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp);
    """
    cursor_base_datos.executescript(consulta_cracion_tabla)
    conexion_sqlite.commit()
    conexion_sqlite.close()

def guardar_registros(lista_registros: List[Dict[str,Any]])-> int:
    """ Guarda una lista de registros (o un registro único convertido a lista) en la base de datos.
    Devuelve la cantidad de registros insertados exitosamente.
    """
    conexion_sqlite=sqlite3.connect(RUTA_BASE_DATOS)
    cursor_base_datos=conexion_sqlite.cursor()

    consulta_insercion="""
    INSERT INTO logs (timestamp, servicio, gravedad, mensaje)
    VALUES (:timestamp, :servicio, :gravedad, :mensaje)
    """

    # executemany permite insertar múltiples diccionarios en una sola transacción
    cursor_base_datos.executemany(consulta_insercion, lista_registros)
    registros_insertados=cursor_base_datos.rowcount

    conexion_sqlite.commit()
    conexion_sqlite.close()

    return registros_insertados

def consultar_registros(
    fecha_inicio: Optional[str]=None,
    fecha_fin: Optional[str]=None,
    )-> List[Dict[str,Any]]:
    """Consulta registros almacenados en la base de datos con soporte opcional de rango de fechas."""
    
    conexion_sqlite=sqlite3.connect(RUTA_BASE_DATOS)
    "SELECT id, timestamp, servicio, gravedad, mensaje FROM logs WHERE 1=1"
    # permie accede a los resutados como diccionarios
    conexion_sqlite.row_factory=sqlite3.Row
    cursor_base_datos=conexion_sqlite.cursor()
    parametros_consulta=[]

    #filtro dinamico por rango de fecha y hora
    if fecha_inicio:
        consulta_sql+="AND timestamp>=?"
        parametros_consulta.append(fecha_inicio)

    if fecha_fin:
            consulta_sql+="AND timestamp<=?"
            parametros_consulta.append(fecha_fin)
    
    consulta_sql+="ORDER BY timestamp DESC"

    cursor_base_datos.execute(consulta_sql,parametros_consulta)
    filas_obtenidas=cursor_base_datos.fetchall()

    # Convertimos cada fila SQLite a un diccionario nativo de Python
    lista_registros_obtenidos=[Dict[fila] for fila in filas_obtenidas]

    conexion_sqlite.close()
    return lista_registros_obtenidos