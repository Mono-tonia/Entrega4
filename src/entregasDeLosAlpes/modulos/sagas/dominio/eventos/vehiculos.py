from __future__ import annotations
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoVehiculo(EventoDominio):
    ...

@dataclass
class ProductoDevuelto(EventoVehiculo):
    id_correlacion: str = None
    producto_id: str = None
    fecha_devolucion: datetime = None

@dataclass
class ProductoEntregado(EventoVehiculo):
    id_correlacion: str = None
    producto_id: str = None
    fecha_entrega: datetime = None
