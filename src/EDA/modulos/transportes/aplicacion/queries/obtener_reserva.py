from EDA.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from EDA.seedwork.aplicacion.queries import ejecutar_query as query
from EDA.modulos.transportes.infraestructura.repositorios import RepositorioDistribucion
from EDA.modulos.transportes.dominio.entidades import Distribucion
from dataclasses import dataclass
from .base import ReservaQueryBaseHandler
from EDA.modulos.transportes.aplicacion.mapeadores import MapeadorDistribucion
import uuid

@dataclass
class ObtenerDistribucion(Query):
    id: str

class ObtenerDistribucionHandler(ReservaQueryBaseHandler):

    def handle(self, query: ObtenerDistribucion) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Distribucion)
        distribucion =  self.fabrica_transporte.crear_objeto(vista.obtener_por(id=query.id)[0], MapeadorDistribucion())
        return QueryResultado(resultado=distribucion)

@query.register(ObtenerDistribucion)
def ejecutar_query_obtener_distribucion(query: ObtenerDistribucion):
    handler = ObtenerDistribucionHandler()
    return handler.handle(query)