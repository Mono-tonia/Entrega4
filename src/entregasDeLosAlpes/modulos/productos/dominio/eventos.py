from __future__ import annotations
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
from .objetos_valor import Ruta
import uuid 

class EventoOrden(EventoDominio):
    ...

@dataclass
class OrdenRecibida(EventoOrden):
    id_orden: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    listaProd: list[any]= None
    fecha_recepcion: datetime = None
    ruta: Ruta = None
    
@dataclass
class OrdenProcesada(EventoOrden):
    id_orden: uuid.UUID = None
    ruta: Ruta = None
    producto: any = None
    fecha_actualizacion: datetime = None
