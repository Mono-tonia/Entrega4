from __future__ import annotations
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoBodega(EventoDominio):
    ...

@dataclass
class EntregaConfirmada(EventoBodega):
    orden_id: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None

@dataclass
class ConfirmacionRevertida(EventoBodega):
    orden_id: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None