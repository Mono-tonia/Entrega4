from __future__ import annotations
from dataclasses import dataclass, field
from EDA.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid 

class EventoCompra(EventoDominio):
    ...

@dataclass
class CompraCreada(EventoCompra):
    id_compra: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    
@dataclass
class CompraCancelada(EventoCompra):
    id_id_compra: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class CompraAprobada(EventoCompra):
    id_compra: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class CompraPagada(EventoCompra):
    id_compra: uuid.UUID = None
    fecha_actualizacion: datetime = None