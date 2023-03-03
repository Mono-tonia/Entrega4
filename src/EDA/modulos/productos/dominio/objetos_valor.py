"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from EDA.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
from datetime import datetime
from enum import Enum



@dataclass(frozen=True)
class Nombre():
    nombre: str

class Categoria(): 
    categoria: str

class EstadoCompra(str, Enum):
    APROBADA = "Aprobada"
    PENDIENTE = "Pendiente"
    CANCELADA = "Cancelada"
    
class Capacidad():
    capacidad:float()

class Direccion():
    direccion:str

class TipoBodega():
    tipoBodega:str