"""Objetos valor del dominio de bodegas

En este archivo usted encontrará los objetos valor del dominio de bodegas

"""

from __future__ import annotations

from dataclasses import dataclass, field 
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Producto
from enum import Enum

@dataclass(frozen=True)
class Nombre():
    nombre: str

class Ubicacion(): 
    ubicacion: str

class Capacidad():
    capacidad: int

class Stock():
    stock: list[Producto]
