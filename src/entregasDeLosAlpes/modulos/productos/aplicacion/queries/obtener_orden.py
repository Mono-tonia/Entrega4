from entregasDeLosAlpes.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from entregasDeLosAlpes.seedwork.aplicacion.queries import ejecutar_query as query
from entregasDeLosAlpes.modulos.productos.dominio.repositorios import RepositorioOrdenes
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Orden
from dataclasses import dataclass
from .base import OrdenQueryBaseHandler
from entregasDeLosAlpes.modulos.productos.aplicacion.mapeadores import MapeadorOrden
import uuid

@dataclass
class ObtenerOrden(Query):
    id: str

class ObtenerOrdenHandler(OrdenQueryBaseHandler):

    def handle(self, query: ObtenerOrden) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Orden)
        orden =  self.fabrica_productos.crear_objeto(vista.obtener_por(id=query.id)[0], MapeadorOrden())
        return QueryResultado(resultado=orden)

@query.register(ObtenerOrden)
def ejecutar_query_obtener_reserva(query: ObtenerOrden):
    handler = ObtenerOrdenHandler()
    return handler.handle(query)