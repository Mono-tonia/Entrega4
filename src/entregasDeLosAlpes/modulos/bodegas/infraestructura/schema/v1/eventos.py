from pulsar.schema import *
from entregasDeLosAlpes.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from entregasDeLosAlpes.seedwork.infraestructura.utils import time_millis
from entregasDeLosAlpes.modulos.bodegas.dominio.entidades import Bodega
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Producto
from entregasDeLosAlpes.modulos.bodegas.dominio.objetos_valor import Stock
import uuid

class CrearAlmacenamientoPayload(Record):
    
    id_cliente = String()
    listaBod = list[Bodega]


class EventoCrearAlmacenamiento(EventoIntegracion):
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
    data = CrearAlmacenamientoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BuscarAlmacenamientoPayload(Record):
    
    bodega = Bodega
    producto = Producto
    stock = Stock

class EventoBuscarAlmacenamiento(EventoIntegracion):
    # NOTE La librería Record de Pulsar no es capaz de reconocer campos heredados, 
    # por lo que los mensajes al ser codificados pierden sus valores
    # Dupliqué el los cambios que ya se encuentran en la clase Mensaje
    id = String(default=str(uuid.uuid4()))
    time = Long()
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = BuscarAlmacenamientoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)