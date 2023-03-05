"""Entidades del dominio de bodegas

En este archivo usted encontrará las entidades del dominio de bodegas

"""

from __future__ import annotations
from dataclasses import dataclass, field

import entregasDeLosAlpes.modulos.bodegas.dominio.objetos_valor as ov
from entregasDeLosAlpes.modulos.bodegas.dominio.eventos import CrearAlmacenamiento, BuscarAlmacenamiento
from entregasDeLosAlpes.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Producto
import uuid


@dataclass
class Bodega(Entidad):
    #atributos: nombre, ubicacion, capacidad, stock de productos
    nombre: ov.Nombre = field(default_factory=ov.Nombre)
    ubicacion: ov.Ubicacion = field(default_factory=ov.Ubicacion)
    capacidad: ov.Capacidad = field(default_factory=ov.Capacidad)
    stock: ov.Stock = field(default_factory=ov.Stock)



@dataclass
class Almacenamiento(AgregacionRaiz):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    listaBod: list[Bodega] = []

    def crear_almacenamiento(self, almacenamiento: Almacenamiento):
        self.id_cliente = almacenamiento.id_cliente
        self.listaBod = almacenamiento.listaBod


        self.agregar_evento(CrearAlmacenamiento(id_orden=self.id, id_cliente=self.id_cliente, estado=self.estado.name, listaProd=self.listaProd, fecha_recepcion=self.fecha_recepcion, ruta=self.ruta))
        #Agregar evento de compensación


    def buscar_almacenamiento(self, producto: Producto):
        
        for bodega in self.listaBod:
            for prod in bodega.stock.stock:
                if prod == producto:
                    self.agregar_evento(BuscarAlmacenamiento(bodega=bodega, producto=producto, stock=bodega.stock))
                    #agregar evento

    def agregar_bodega(self, bodega: Bodega):
        self.listaBod.append(bodega)
        #Agregar evento de compensación

    def eliminar_bodega(self, bodega: Bodega):
        self.listaBod.remove(bodega)
        
