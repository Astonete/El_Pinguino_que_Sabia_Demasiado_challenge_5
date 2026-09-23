from flask import Flask, request, jsonify
from datetime import datetime, timezone
import json
import sys
import os

# permitir la importacion del modulo de base de datos desde la carpeta hermana
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'base_datos'))
from base_de_datos.gestor_base_datos import(
    inicializar_base_de_datos,
    guardar_registros,
    consultar_registros
    )

aplicacion_servidor = Flask(__name__)

# Lista manual de tokens autorizados mapeados al servicio correspondiente
DICCIONARIO_TOKENS_VALIDOS = {
    "token-servicio-autenticacion-789":"servicio_autenticacion",
    "token-servicio-pago-456": "servicio_pago",
    "token-servicio-inventario-123": "servicio_inventario"
}

def validar_token_autorizacion(cabecera_autorizacion: str)->bool:
    """
    Verifica si el encabezado Authorization contiene un token registrado.
    Formato esperado: "token VALOR_DEL_TOKEN"
    """
    if not cabecera_autorizacion:
        return False
    
    partes_cabecera = cabecera_autorizacion.split()
    if len(partes_cabecera) != 2 or partes_cabecera[0].lower() != "token":
        return False
    
    token_extraido= partes_cabecera[1]
    return token_extraido in DICCIONARIO_TOKENS_VALIDOS

@aplicacion_servidor.route('/registro', methods=['POST'])
def recibir_peticion():
    """
    Endpoint POST /logs
    Recibe registros en JSON (un solo registro o una lista de ellos) y los almacena.
    """
    cabecera_autorizacion = request.headers.get('Authorization')
    
    #1 verificacion de autenticacion
    if not validar_token_autorizacion(cabecera_autorizacion):
        return jsonify({"estado":"error",
                        "mensaje":"Ndepio Ma'a: puede que no tengas token, o el token sea mas falso que tu personalidad"
                    }),401
    datos_json_recibidos=request.get_json()
    if not datos_json_recibidos:
        return jsonify({"estado":"error",
                        "mensaje":"Peticion Invalida: Si no va ser un archivo JSON deja nomas ya no quiero"
                    }),400
        
    # Normalizamos  el dato recibido para procesar un solo dict o una lista de dicts
    if isinstance(datos_json_recibidos, dict):
        lista_logs_a_guardar = [datos_json_recibidos]
    elif isinstance(datos_json_recibidos, list):
        lista_logs_a_guardar = datos_json_recibidos
    else:
        return jsonify({"estado":"error",
                        "mensaje":"Formato no soportado: dame un Objeto JSON o una lista"
                    }),400

    # 2. Validación de campos obligatorios en cada registro
    campos_requeridos = {"timestamp","servicio","gravedad","mensaje"}
    for registro in lista_logs_a_guardar:
        if not campos_requeridos.issubset(registro.keys()):
            return jsonify({"estado":"error",
                            "mensaje":f"Registro Incompleto por estructura invalida: faltan campos requeridos cada resgistro debe incluir {campos_requeridos}"
                        }),400
    
    # 3. Guardado en Base de Datos
    cantidad_guardada=guardar_registros(lista_logs_a_guardar)
    
    return jsonify({
        "estado":"exito",
        "mensaje": f"se procesaron y almacenaron {cantidad_guardada} registros de log correctamente"
    }),201

@aplicacion_servidor.route('/logs', methods=['GET'])
def obtener_registros():
    """
    Endpoint GET /logs
    Permite consultar logs almacenados filtrando por 'fecha_inicio' y 'fecha_fin'
    Ejemplo: GET /logs?fecha_inicio=2026-09-01T00:00:00&fecha_fin=2026-09-30T23:59:59
    """
    fecha_inicio_filtro = request.args.get('fecha_inicio')
    fecha_fin_filtro = request.args.get('fecha_fin')

    registros_encontrados = consultar_registros