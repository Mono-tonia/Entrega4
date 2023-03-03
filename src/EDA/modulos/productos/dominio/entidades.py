"""Entidades del dominio de productos

En este archivo usted encontrará las entidades del dominio de productos

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import EDA.modulos.productos.dominio.objetos_valor as ov
from EDA.modulos.productos.dominio.eventos import CompraCreada, CompraAprobada, CompraCancelada, CompraPagada
from EDA.seedwork.dominio.entidades import Locacion, AgregacionRaiz, Entidad
import uuid

@dataclass
class Compra(Entidad):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)

@dataclass
class Bodega(Entidad):
    tipoBodega: ov.TipoBodega = field(default_factory=ov.TipoBodega)
    capacidad: ov.Capacidad = field(default_factory=ov.Capacidad)
    direccion: ov.Direccion = field(default_factory=ov.Direccion)

@dataclass
class Compra(AgregacionRaiz):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoCompra = field(default=ov.EstadoCompra.PENDIENTE)

    def crear_compra(self, compra: Compra):
        self.id_cliente = compra.id_cliente
        self.estado = compra.estado
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(CompraCreada(id_compra=self.id, id_cliente=self.id_cliente, estado=self.estado.name, fecha_creacion=self.fecha_creacion))
        # TODO Agregar evento de compensación

    def aprobar_compra(self):
        self.estado = ov.EstadoCompra.APROBADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(CompraAprobada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación

    def cancelar_compra(self):
        self.estado = ov.EstadoCompra.CANCELADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(CompraCancelada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación
    
    def pagar_compra(self):
        self.estado = ov.EstadoCompra.PAGADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(CompraPagada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación
