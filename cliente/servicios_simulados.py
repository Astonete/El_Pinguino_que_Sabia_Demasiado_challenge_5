import requests
import random
import time
from datetime import datetime
from typing import Dict, Any, List

URL_SERVIDOR_CENTRAL =  "http://localhost:5000/logs"

# Configuración de servicios con sus tokens legítimos asignados
SERVICIOS_CONFIGURADOS = [
    {
        "nombre":"servicio_autenticacion",
        "token":"token-servicio-autenticacion-789",
        "mensajes":[
            ("INFO","Usuario 'dovahkiin' inicio de sesion exitosamente"),
            ("WARNING","Intento fallido de inicio de sesion para el usuario 'admin'"),
            ("ERROR","Servicio de LDAP no responde al validar credenciales")
        ]
    },
    {
            "nombre":"servicio_pagos",
            "token":"token-servicio-pagos-456",
            "mensajes":[
                ("INFO","Procesado de pago por Gs150.000 guaranies con tarjeta Ueno Bank"),
                ("ERROR","Pasarela de pago Stripe devolvio error 502 Bad Gateway"),
                ("CRITICAL","FALLO Catastrofico al reintentar transaccion de cobro anual")
            ]
    },
    {
        "nombre":"servicio_inventario",
        "token":"token-servicio-inventario-123",
        "mensajes":[
            ("INFO","Stock actualizado para producto ID-8821"),
            ("DEBUG","Verificando disponibilidad en bodega central para orden #4021"),
            ("WARNING","inventario critico para categoria 'Laptops'"),
        ]
    }
]

def crear_registro_falso(servicio_info:Dict[str,Any])-> Dict[str,Any]:
    """Genera un diccionario con la estructura válida de un registro de log."""
    gravedad, mensaje_plantilla = random.choice(servicio_info["mensajes"])

    return{
        "timestamp":datetime.now().isoformat(),
        "servicio":servicio_info["nombre"],
        "gravedad":gravedad,
        "mensaje":mensaje_plantilla
    }

def enviar_log_al_servidor(registro_log: Dict[str,Any], token_autenticacion:str)->None:
    """ Envía un único registro de log por método HTTP POST con el encabezado de autorización."""
    encabezado_http={
        "Content-Type":"application/json",
        "Authorization":f"token{token_autenticacion}"
    }

    try:
        respuesta_servidor= requests.post(
            URL_SERVIDOR_CENTRAL,
            json=registro_log,
            headers=encabezado_http,
            timeout=3
        )
        print(f"[{registro_log['servicio']}] Codigo HTTP: {respuesta_servidor.status_code} -> {respuesta_servidor.json()['mensaje']}")
    except requests.exceptions.RequestException as error_conexion:
        print(f"    Error de conexion al enviar log: {error_conexion}")

def envia_lote_logs(lista_registros: List[Dict[str,Any]],token_autenticacion:str)->None:
    """Demuestra el envío múltiple (batch) de registros en una sola llamada HTTP POST."""
    encabezado_http={
            "Content-Type":"application/json",
            "Authorization":f"token{token_autenticacion}"
        }

    try:
            respuesta_servidor= requests.post(
                URL_SERVIDOR_CENTRAL,
                json=lista_registros,
                headers=encabezado_http,
                timeout=3
            )
            print(f"\n ENVIO DE LOTE ({len(lista_registros)} logs) -> HTTP {respuesta_servidor.status_code}: {respuesta_servidor.json()['mensaje']}\n")
    except requests.exceptions.RequestException as error_conexion:
        print(f"Error enviando lote: {error_conexion}")

def probar_token_invalidos()->None:
    """Prueba de seguridad: Intenta enviar un log con un token falso para validar la respuesta 401 del servidor."""
    print("\n --- PRUEBA DE SEGURIDAD: Probando Token Inválido ---")
    encabezados_invalidos={
        "Content-Type":"application/json",
        "Authorization":"token_ESTE_TOKEN_ES_FALSO_123"
    }
    log_prueba = {
        "timestamp": datetime.now().isoformat(),
        "servicio":"servicio_hack",
        "gravedad":"CRITICAL",
        "mensaje":"Intento de Infiltracion"
    }

    respuesta= requests.post(URL_SERVIDOR_CENTRAL, json=log_prueba,headers=encabezados_invalidos)
    print(f"Respuesta del Servidor a token Invalidos: Status {respuesta.status_code}")
    print(f"Detalle de Error: {respuesta.json()}\n")

    def ejecutar_simulacion():
        print ("===< Iniciando simulacion de servicios emisores de logs >===")

    #1. enviar registros individuales aleatorios
    for _ in range(5):
        servicio_elegido=random.choice(SERVICIOS_CONFIGURADOS)
        log_generador=crear_registro_falso(servicio_elegido)
        enviar_log_al_servidor(log_generador, servicio_elegido["token"])
        time.sleep(0.5)

    #2. probar en lote
    servicio_lote = random.choice(SERVICIOS_CONFIGURADOS)
    log_generador = [crear_registro_falso(servicio_lote) for _ in range(3)]

    #3. Probar rechazo de Token Invalido
    probar_token_invalidos()

    if __name__=='__main__':
        ejecutar_simulacion()