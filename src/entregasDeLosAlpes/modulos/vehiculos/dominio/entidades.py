"""Entidades del dominio de vehiculos

En este archivo usted encontrará las entidades del dominio de vehiculos

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import entregasDeLosAlpes.modulos.vehiculos.dominio.objetos_valor as ov
from entregasDeLosAlpes.modulos.vehiculos.dominio.eventos import ProductoEntregado, ProductoRecibido
from entregasDeLosAlpes.seedwork.dominio.entidades import  AgregacionRaiz, Entidad

@dataclass
class Producto(Entidad):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.Nombre = field(default_factory=ov.Nombre)
    categoria: ov.Categoria = field(default_factory=ov.Categoria)

@dataclass
class Proveedor(Entidad):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreProveedor = field(default_factory=ov.NombreProveedor)
    
@dataclass
class Transporte(AgregacionRaiz):
    estado: ov.EstadoCargamento = field(default=ov.EstadoCargamento.CARGADO)
    listaProd: list[Producto]  = field(default_factory=list[Producto])
    ruta : ov.Ruta = field(default=ov.Ruta)

    def recibir_producto(self, transporte: Transporte):
        self.id_bodega = transporte.id_bodega
        self.estado = ov.EstadoCargamento.EN_CAMINO
        self.listaProd=transporte.listaProd
        self.fecha_recepcion = datetime.datetime.now()    
        self.ruta= transporte.ruta
        for produto_act in self.listaProd:
            self.agregar_evento(ProductoRecibido(id_transporte=self.id, id_bodega=self.id_bodega, producto=produto_act, fecha_recepcion=self.fecha_recepcion, ruta=self.ruta))
        # TODO Agregar evento de compensación

    def entregar_producto(self, transporte: Transporte):
        self.estado = ov.EstadoCargamento.DESPACHADO
        self.listaProd=transporte.listaProd
        self.fecha_entrega = datetime.datetime.now()   
        
        for produto_act in self.listaProd:
            self.agregar_evento(ProductoEntregado(id_transporte=self.id, producto=produto_act, fecha_entrega=self.fecha_entrega))
        # TODO Agregar evento de compensación


#########################   NO SABEMOS COMO RELACIONARLO CON BODEGA

