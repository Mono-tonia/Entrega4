from pulsar.schema import *
from .utils import time_millis
import uuid

class ConfirmarEntregaPayload(Record):
    id_correlacion = String(),
    orden_id = String(),
 
class RevertirConfirmacionPayload(Record):
    id = String()
    id_correlacion = String()
    orden_id = String()

class ComandoConfirmarEntrega(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="ConfirmarEntrega")
    datacontenttype = String()
    service_name = String(default="bodegas.entregasDeLosAlpes")
    data = ConfirmarEntregaPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComandoRevertirConfirmacion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="RevertirConfirmacion")
    datacontenttype = String()
    service_name = String(default="bodegas.entregasDeLosAlpes")
    data = RevertirConfirmacionPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
