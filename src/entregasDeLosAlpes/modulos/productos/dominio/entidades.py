"""Entidades del dominio de productos

En este archivo usted encontrará las entidades del dominio de productos

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import entregasDeLosAlpes.modulos.productos.dominio.objetos_valor as ov
from entregasDeLosAlpes.modulos.productos.dominio.eventos import OrdenRecibida, OrdenProcesada
from entregasDeLosAlpes.seedwork.dominio.entidades import AgregacionRaiz, Entidad
import uuid


@dataclass
class Producto(Entidad):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.Nombre = field(default_factory=ov.Nombre)
    categoria: ov.Categoria = field(default_factory=ov.Categoria)


@dataclass
class Orden(AgregacionRaiz):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoOrden = field(default=ov.EstadoOrden.RECIBIDA)
    listaProd: list[Producto] = []
    ruta : ov.Ruta = field(default=ov.ruta)

    def recibir_orden(self, orden: Orden):
        self.id_cliente = orden.id_cliente
        self.estado = ov.EstadoOrden.RECIBIDA
        self.listaProd=orden.listaProd
        self.fecha_recepcion = datetime.datetime.now()    
        self.ruta= orden.ruta

        self.agregar_evento(OrdenRecibida(id_orden=self.id, id_cliente=self.id_cliente, estado=self.estado.name, listaProd=self.listaProd, fecha_recepcion=self.fecha_recepcion, ruta=self.ruta))
        # TODO Agregar evento de compensación

    def procesar_orden(self):
        self.estado = ov.EstadoOrden.PROCESADA
        self.fecha_actualizacion = datetime.datetime.now()
        
        for produto_act in self.listaProd:
            self.agregar_evento(OrdenProcesada(self.id, self.ruta, produto_act,self.fecha_actualizacion))
        # TODO Agregar evento de compensación
