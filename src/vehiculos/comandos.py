from pulsar.schema import *
from .utils import time_millis
import uuid

class EntregarProductoPayload(Record):
    id_correlacion = String(),
    producto_id = String(),
    fecha_entrega = Long()
 
class DevolverProductoPayload(Record):
    id = String()
    id_correlacion = String()
    producto_id = String()

class ComandoEntregarProducto(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="ComandoEntregarProducto")
    datacontenttype = String()
    service_name = String(default="vehiculos.entregasDeLosAlpes")
    data = EntregarProductoPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComandoDevolverProducto(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="DevolverProducto")
    datacontenttype = String()
    service_name = String(default="vehiculos.entregasDeLosAlpes")
    data = DevolverProductoPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
