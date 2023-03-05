"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field 
from datetime import datetime
from entregasDeLosAlpes.seedwork.dominio.objetos_valor import Locacion
from enum import Enum

@dataclass(frozen=True)
class Nombre():
    nombre: str

class Categoria(): 
    categoria: str

class Codigo():
    codigo: str

class EstadoOrden(str, Enum):
    RECIBIDA = "Recibida"
    PROCESADA = "Procesada"

@dataclass(frozen=True)
class Ruta:
    fecha_salida: datetime
    fecha_llegada: datetime
    origen: Locacion
    destino: Locacion

    def origen(self) -> Locacion:
        return self.origen

    def destino(self) -> Locacion:
        return self.destino

    def fecha_salida(self) -> datetime:
        return self.fecha_salida
    
    def fecha_llegada(self) -> datetime:
        return self.fecha_llegada

