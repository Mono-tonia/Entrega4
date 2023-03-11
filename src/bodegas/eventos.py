from pulsar.schema import *
from .utils import time_millis
import uuid

class EntregaConfirmada(Record):
    id = String(),
    id_correlacion = String(),
    orden_id = String()
    fecha_confirmacion = Long()
 
class ConfirmacionRevertida(Record):
    id = String()
    id_correlacion = String()
    orden_id = String()
    fecha_actualizacion = Long()

class EventoConfirmacionBodega(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoBodega")
    datacontenttype = String()
    service_name = String(default="bodegas.entregasDeLosAlpes")
    confirmacion_revertida = ConfirmacionRevertida
    entrega_confirmada = EntregaConfirmada

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
