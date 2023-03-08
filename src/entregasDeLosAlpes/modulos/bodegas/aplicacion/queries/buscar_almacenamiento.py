from entregasDeLosAlpes.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from entregasDeLosAlpes.seedwork.aplicacion.queries import ejecutar_query as query
from entregasDeLosAlpes.modulos.bodegas.dominio.repositorios import RepositorioAlmacenamiento
from entregasDeLosAlpes.modulos.bodegas.dominio.entidades import Almacenamiento
from dataclasses import dataclass
from .base import AlmacenamientoQueryBaseHandler
from entregasDeLosAlpes.modulos.bodegas.aplicacion.mapeadores import MapeadorAlmacenamiento
import uuid

@dataclass
class BuscarAlmacenamiento(Query):
    id: str

class BuscaralmacenamientoHandler(AlmacenamientoQueryBaseHandler):

    def handle(self, query: BuscarAlmacenamiento) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Almacenamiento)
        almacenamiento =  self.fabrica_bodegas.crear_objeto(vista.obtener_por(id=query.id)[0], MapeadorAlmacenamiento())
        return QueryResultado(resultado=almacenamiento)

@query.register(BuscarAlmacenamiento)
def ejecutar_query_obtener_almacenamiento(query: BuscarAlmacenamiento):
    handler = AlmacenamientoQueryBaseHandler()
    return handler.handle(query)