""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vehiculos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vehiculos

"""

from entregasDeLosAlpes.config.db import db
from entregasDeLosAlpes.modulos.vehiculos.dominio.repositorios import RepositorioTransportes, RepositorioProveedores, RepositorioEventosTransportes
from entregasDeLosAlpes.modulos.vehiculos.dominio.objetos_valor import NombreProveedor, Codigo
from entregasDeLosAlpes.modulos.vehiculos.dominio.entidades import Proveedor, Transporte
from entregasDeLosAlpes.modulos.vehiculos.dominio.fabricas import FabricaVehiculos
from .dto import Transportes as TransporteDTO
from .dto import EventosTransporte
from .mapeadores import MapeadorTransporte, MapadeadorEventosTransporte
from uuid import UUID
from pulsar.schema import *

class RepositorioProveedoresSQLAlchemy(RepositorioProveedores):

    def obtener_por_id(self, id: UUID) -> Transporte:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Transporte]:
        proveedor = Proveedor(codigo=Codigo(codigo="ter"), nombre=NombreProveedor(nombre= "Terceros"))
        return [proveedor]

    def agregar(self, entity: Transporte):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: Transporte):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError


class RepositorioTransportesSQLAlchemy(RepositorioTransportes):

    def __init__(self):
        self._fabrica_vehiculos: FabricaVehiculos = FabricaVehiculos()

    @property
    def fabrica_vehiculos(self):
        return self._fabrica_vehiculos

    def obtener_por_id(self, id: UUID) -> Transporte:
        transporte_dto = db.session.query(TransporteDTO).filter_by(id=str(id)).one()
        return self.fabrica_vehiculos.crear_objeto(transporte_dto, MapeadorTransporte())

    def obtener_todos(self) -> list[Transporte]:
        # TODO
        raise NotImplementedError

    def agregar(self, transporte: Transporte):
        transporte_dto = self.fabrica_vehiculos.crear_objeto(transporte, MapeadorTransporte())

        db.session.add(transporte_dto)

    def actualizar(self, transporte: Transporte):
        # TODO
        raise NotImplementedError

    def eliminar(self, transporte_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosTransporteSQLAlchemy(RepositorioEventosTransportes):

    def __init__(self):
        self._fabrica_vehiculos: FabricaVehiculos = FabricaVehiculos()

    @property
    def fabrica_vehiculos(self):
        return self._fabrica_vehiculos

    def obtener_por_id(self, id: UUID) -> Transporte:
        transporte_dto = db.session.query(TransporteDTO).filter_by(id=str(id)).one()
        return self.fabrica_vehiculos.crear_objeto(transporte_dto, MapadeadorEventosTransporte())

    def obtener_todos(self) -> list[Transporte]:
        raise NotImplementedError

    def agregar(self, evento):
        transporte_evento = self.fabrica_vehiculos.crear_objeto(evento, MapadeadorEventosTransporte())

        parser_payload = JsonSchema(transporte_evento.data.__class__)
        json_str = parser_payload.encode(transporte_evento.data)

        evento_dto = EventosTransporte()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_transporte)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(transporte_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(transporte_evento.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, transporte: Transporte):
        raise NotImplementedError

    def eliminar(self, transporte_id: UUID):
        raise NotImplementedError
