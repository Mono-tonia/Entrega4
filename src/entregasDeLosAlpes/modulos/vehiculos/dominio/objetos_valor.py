"""Objetos valor del dominio de vehiculos

En este archivo usted encontrará los objetos valor del dominio de vehiculos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
from datetime import datetime
from enum import Enum



@dataclass(frozen=True)
class NombreProveedor():
    nombre: str

@dataclass(frozen=True)
class Ruta:
    fecha_salida: datetime
    fecha_llegada: datetime
    destino: Locacion

    def destino(self) -> Locacion:
        return self.destino

    def fecha_salida(self) -> datetime:
        return self.fecha_salida
    
    def fecha_llegada(self) -> datetime:
        return self.fecha_llegada

class TipoCargamento(Enum):
    REFRIGERADOS= "Refrigerados"
    COMIDA = "Comida"
    PRODUCTOS = "Productos"


class EstadoCargamento(str, Enum):
    CARGADO = "Cargado"
    EN_CAMINO = "EnCamino"
    DESPACHADO = "Despachado"
