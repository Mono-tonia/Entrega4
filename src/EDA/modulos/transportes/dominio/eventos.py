from __future__ import annotations
from dataclasses import dataclass, field
from EDA.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoDistribucion(EventoDominio):
    ...

@dataclass
class DistribucionIniciada(EventoDominio):
    id_distribucion: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    
@dataclass
class DistribucionTerminada(EventoDominio):
    id_distribucion: uuid.UUID = None
    fecha_actualizacion: datetime = None