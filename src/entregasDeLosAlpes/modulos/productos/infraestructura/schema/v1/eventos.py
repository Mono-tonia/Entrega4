from pulsar.schema import *
from entregasDeLosAlpes.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from entregasDeLosAlpes.seedwork.infraestructura.utils import time_millis
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Producto
from entregasDeLosAlpes.modulos.productos.dominio.objetos_valor import Ruta
import uuid

class OrdenRecibidaPayload(Record):
    id_orden = String()
    id_cliente = String()
    estado = String()
    fecha_recepcion = Long()

class EventoOrdenRecibida(EventoIntegracion):
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
    data = OrdenRecibidaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class OrdenProcesadaPayload(Record):
    id_orden = String()
    id_cliente = String()
    estado = String()
    producto = Producto()
    ruta = Ruta()

class EventoOrdenProcesada(EventoIntegracion):
    # NOTE La librería Record de Pulsar no es capaz de reconocer campos heredados, 
    # por lo que los mensajes al ser codificados pierden sus valores
    # Dupliqué el los cambios que ya se encuentran en la clase Mensaje
    id = String(default=str(uuid.uuid4()))
    time = Long()
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = OrdenProcesadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)