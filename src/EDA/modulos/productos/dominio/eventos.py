from __future__ import annotations
from dataclasses import dataclass, field
from EDA.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoPedido(EventoDominio):
    ...

@dataclass
class PedidoCreada(EventoPedido):
    id_pedido: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    
@dataclass
class PedidoCancelada(EventoPedido):
    id_id_pedido: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class PedidoAprobada(EventoPedido):
    id_pedido: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class PedidoPagada(EventoPedido):
    id_pedido: uuid.UUID = None
    fecha_actualizacion: datetime = None