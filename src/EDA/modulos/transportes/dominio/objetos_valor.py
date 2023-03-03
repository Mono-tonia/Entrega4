"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from EDA.seedwork.dominio.objetos_valor import ObjetoValor, Ruta, Locacion
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class NombreTercero():
    nombre: str

@dataclass(frozen=True)
class Leg(Ruta):
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

@dataclass(frozen=True)
class Segmento(Ruta):
    legs: list[Leg]

    def origen(self) -> Locacion:
        return self.legs[0].origen

    def destino(self) -> Locacion:
        return self.legs[-1].destino

    def fecha_salida(self) -> datetime:
        return self.legs[0].fecha_salida
    
    def fecha_llegada(self) -> datetime:
        return self.legs[-1].fecha_llegada

@dataclass(frozen=True)
class Producto(ObjetoValor):
    odos: list[Odo] = field(default_factory=list)
    #proveedor: 'Proveedor' = field(default_factory='Proveedor')

    def ruta(self):
        return f"{str(self.odos[0].origen())}-{str(self.odos[0].destino())}"

@dataclass(frozen=True)
class Odo(Ruta):
    segmentos: list[Segmento]

    def origen(self) -> Locacion:
        return self.segmentos[0].origen

    def destino(self) -> Locacion:
        return self.segmentos[-1].destino

    def fecha_salida(self):
        return self.segmentos[0].fecha_salida()

    def fecha_llegada(self):
        return self.segmentos[-1].fecha_llegada()


class EstadoDistribucion(str, Enum):
    PENDIENTE = "Pendiente"
    TERMINADA = "Terminada"