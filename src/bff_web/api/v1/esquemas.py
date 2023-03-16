import typing
import strawberry
import uuid
import requests
import os

from datetime import datetime


ENTREGAS_HOST = os.getenv("ENTREGAS_ADDRESS", default="localhost")
FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

def obtener_ordenes(root) -> typing.List["Orden"]:
    ordenes_json = requests.get(f'http://{ENTREGAS_HOST}:5000/productos/orden').json()
    ordenes = []

    for orden in ordenes_json:
        ordenes.append(
            Orden(
                id=orden.get('id'), 
                id_cliente=orden.get('id_cliente', ''),
                estado=orden.get('estado'),
                listaProd=orden.get('listaProd'), 
                ruta=orden.get('ruta')
            )
        )

    return ordenes

@strawberry.type
class Producto:
    codigo: str 
    nombre: str
    categoria: str

@strawberry.type
class Ruta:
    fecha_salida: str
    fecha_llegada: str
    origen: dict
    destino: dict

@strawberry.type
class Orden:
    id: str
    id_cliente: str   
    estado: str
    listaProd: list[Producto]
    ruta: Ruta

@strawberry.type
class OrdenRespuesta:
    mensaje: str
    codigo: int






