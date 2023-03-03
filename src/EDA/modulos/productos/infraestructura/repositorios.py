""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de productos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de productos

"""

from EDA.config.db import db
from EDA.modulos.productos.dominio.repositorios import RepositorioCompras, RepositorioProveedores, RepositorioEventosCompras
from EDA.modulos.productos.dominio.objetos_valor import TipoBodega 
from EDA.modulos.productos.dominio.entidades import Proveedor, Bodega, Compra
from EDA.modulos.productos.dominio.fabricas import FabricaProductos
from .dto import Compra as CompraDTO
from .dto import EventosCompra
from .mapeadores import MapeadorCompra, MapadeadorEventosCompra
from uuid import UUID
from pulsar.schema import *

class RepositorioProveedoresSQLAlchemy(RepositorioProveedores):

    def obtener_por_id(self, id: UUID) -> Compra:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Compra]:
        #destino=Aeropuerto(codigo="JFK", nombre="JFK International Airport")
        

        proveedor = Proveedor( tipoBodega=TipoBodega(tipoBodega= "Lácteos"))
        return [proveedor]

    def agregar(self, entity: Compra):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: Compra):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError


class RepositorioComprasSQLAlchemy(RepositorioCompras):

    def __init__(self):
        self._fabrica_productos: FabricaProductos = FabricaProductos()

    @property
    def fabrica_productos(self):
        return self._fabrica_productos

    def obtener_por_id(self, id: UUID) -> Compra:
        reserva_dto = db.session.query(CompraDTO).filter_by(id=str(id)).one()
        return self.fabrica_productos.crear_objeto(reserva_dto, MapeadorCompra())

    def obtener_todos(self) -> list[Compra]:
        # TODO
        raise NotImplementedError

    def agregar(self, reserva: Compra):
        reserva_dto = self.fabrica_productos.crear_objeto(reserva, MapeadorCompra())

        db.session.add(reserva_dto)

    def actualizar(self, reserva: Compra):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosCompraSQLAlchemy(RepositorioEventosCompras):

    def __init__(self):
        self._fabrica_productos: FabricaProductos = FabricaProductos()

    @property
    def fabrica_productos(self):
        return self._fabrica_productos

    def obtener_por_id(self, id: UUID) -> Compra:
        reserva_dto = db.session.query(CompraDTO).filter_by(id=str(id)).one()
        return self.fabrica_productos.crear_objeto(reserva_dto, MapadeadorEventosCompra())

    def obtener_todos(self) -> list[Compra]:
        raise NotImplementedError

    def agregar(self, evento):
        reserva_evento = self.fabrica_productos.crear_objeto(evento, MapadeadorEventosCompra())

        parser_payload = JsonSchema(reserva_evento.data.__class__)
        json_str = parser_payload.encode(reserva_evento.data)

        evento_dto = EventosCompra()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_reserva)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(reserva_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(reserva_evento.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, reserva: Compra):
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        raise NotImplementedError
