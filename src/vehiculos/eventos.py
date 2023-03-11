from pulsar.schema import *
from .utils import time_millis
import uuid

class ProductoEntregado(Record):
    id = String(),
    id_correlacion = String(),
    producto_id = String()
    fecha_entrega = Long()
 
class ProductoDevuelto(Record):
    id = String()
    id_correlacion = String()
    producto_id = String()
    fecha_devolucion = Long()

class EventoVehiculo(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoVehiculo")
    datacontenttype = String()
    service_name = String(default="vehiculos.entregasDeLosAlpes")
    producto_devuelto = ProductoDevuelto
    producto_entregado = ProductoEntregado

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
