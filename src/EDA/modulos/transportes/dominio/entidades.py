"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import EDA.modulos.transportes.dominio.objetos_valor as ov
from EDA.modulos.transportes.dominio.eventos import DistribucionIniciada, DistribucionTerminada
from EDA.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class Proveedor(Entidad):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreTercero = field(default_factory=ov.NombreTercero)

@dataclass
class Distribucion(AgregacionRaiz):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoDistribucion = field(default=ov.EstadoDistribucion.PENDIENTE)
    productos: list[ov.Producto] = field(default_factory=list[ov.Producto])

    def iniciar_distribucion(self, distribucion: Distribucion):
        self.id_cliente = distribucion.id_cliente
        self.estado = distribucion.estado
        self.productos = distribucion.productos
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(DistribucionIniciada(id_reserva=self.id, id_cliente=self.id_cliente, estado=self.estado.name, fecha_creacion=self.fecha_creacion))
        # TODO Agregar evento de compensación

    def terminar_distribucion(self):
        self.estado = ov.EstadoDistribucion.TERMINADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(DistribucionTerminada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación

