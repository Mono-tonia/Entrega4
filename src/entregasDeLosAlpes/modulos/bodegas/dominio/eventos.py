from __future__ import annotations
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.dominio.eventos import (EventoDominio)
import uuid 

class EventoAlmacenamiento(EventoDominio):
    ...

@dataclass
class CrearAlmacenamiento(EventoAlmacenamiento):
    #id_almacenamiento: uuid.UUID = None
    id_cliente: uuid.UUID = None
    listaBod: list[any]= None
    
@dataclass
class BuscarAlmacenamiento(EventoAlmacenamiento):
    bodega: any = None
    producto: any = None
    stock: any = None
