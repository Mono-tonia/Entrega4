from pulsar.schema import *
from entregasDeLosAlpes.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from entregasDeLosAlpes.modulos.vehiculos.dominio.entidades import Producto
from entregasDeLosAlpes.modulos.vehiculos.dominio.objetos_valor import Ruta
from entregasDeLosAlpes.seedwork.infraestructura.utils import time_millis
import uuid

class ProductoRecibidoPayload(Record):
    id_transporte = String()
    id_bodega = String()
    producto = Producto
    fecha_recepcion = Long()
    ruta = Ruta()

class EventoProductoRecibido(EventoIntegracion):
    # NOTE La librería Record de Pulsar no es capaz de reconocer campos heredados, 
    # por lo que los mensajes al ser codificados pierden sus valores
    # Dupliqué el los cambios que ya se encuentran en la clase Mensaje
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ProductoRecibidoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProductoEntregadoPayload(Record):
    id_transporte = String()
    id_cliente = String()
    producto = Producto
    fecha_entrega = Long()

class EventoProductoEntregado(EventoIntegracion):
    # NOTE La librería Record de Pulsar no es capaz de reconocer campos heredados, 
    # por lo que los mensajes al ser codificados pierden sus valores
    # Dupliqué el los cambios que ya se encuentran en la clase Mensaje
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ProductoEntregadoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)