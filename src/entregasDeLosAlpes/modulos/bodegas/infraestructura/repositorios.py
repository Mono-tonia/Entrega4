""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de productos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de productos

"""

from entregasDeLosAlpes.config.db import db
from entregasDeLosAlpes.modulos.bodegas.dominio.repositorios import RepositorioAlmacenamiento, RepositorioEventosAlmacenamiento
from entregasDeLosAlpes.modulos.bodegas.dominio.entidades import  Almacenamiento, Bodega
from entregasDeLosAlpes.modulos.bodegas.dominio.fabricas import FabricaBodegas
from .dto import Almacenamiento as AlmacenamientoDTO
from .dto import EventosAlmacenamiento
from .mapeadores import MapeadorAlmacenamiento, MapadeadorEventosAlmacenamiento
from uuid import UUID
from pulsar.schema import *



class RepositorioAlmacenamientoSQLAlchemy(RepositorioAlmacenamiento):

    def __init__(self):
        self._fabrica_bodegas: FabricaBodegas = FabricaBodegas()

    @property
    def fabrica_bodegas(self):
        return self._fabrica_bodegas

    def obtener_por_id(self, id: UUID) -> Almacenamiento:
        almacenamiento_dto = db.session.query(AlmacenamientoDTO).filter_by(id=str(id)).one()
        return self.fabrica_bodegas.crear_objeto(almacenamiento_dto, MapeadorAlmacenamiento())

    def obtener_todos(self) -> list[Almacenamiento]:
        # TODO
        raise NotImplementedError

    def agregar(self, almacenamiento: Almacenamiento):
        almacenamiento_dto = self.fabrica_bodegas.crear_objeto(almacenamiento, MapeadorAlmacenamiento())

        db.session.add(almacenamiento_dto)

    def actualizar(self, almacenamiento: Almacenamiento):
        # TODO
        raise NotImplementedError

    def eliminar(self, almacenamiento_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosAlmacenamientoSQLAlchemy(RepositorioEventosAlmacenamiento):

    def __init__(self):
        self._fabrica_bodegas: FabricaBodegas = FabricaBodegas()

    @property
    def fabrica_bodegas(self):
        return self._fabrica_bodegas

    def obtener_por_id(self, id: UUID) -> Almacenamiento:
        almacenamiento_dto = db.session.query(AlmacenamientoDTO).filter_by(id=str(id)).one()
        return self.fabrica_bodegas.crear_objeto(almacenamiento_dto, MapadeadorEventosAlmacenamiento())

    def obtener_todos(self) -> list[Almacenamiento]:
        raise NotImplementedError

    def agregar(self, evento):
        almacenamiento_evento = self.fabrica_bodegas.crear_objeto(evento, MapadeadorEventosAlmacenamiento())

        parser_payload = JsonSchema(almacenamiento_evento.data.__class__)
        json_str = parser_payload.encode(almacenamiento_evento.data)

        evento_dto = EventosAlmacenamiento()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_orden)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(almacenamiento_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(almacenamiento_evento.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, orden: Almacenamiento):
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        raise NotImplementedError
