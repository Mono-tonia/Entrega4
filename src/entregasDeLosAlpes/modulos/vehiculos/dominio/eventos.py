from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from entregasDeLosAlpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
from entregasDeLosAlpes.modulos.vehiculos.dominio.objetos_valor import Ruta

class EventoTransporte(EventoDominio):
    ...

@dataclass
class ProductoRecibido(EventoTransporte):
    id_transporte: uuid.UUID = None
    id_bodega: uuid.UUID = None
    producto: any = None
    fecha_recepcion: datetime = None
    ruta: Ruta  = None
    
@dataclass
class ProductoEntregado(EventoTransporte):
    id_transporte: uuid.UUID = None
    producto: any = None
    fecha_entrega: datetime = None

