from entregasDeLosAlpes.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from entregasDeLosAlpes.seedwork.aplicacion.queries import ejecutar_query as query
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.repositorios import RepositorioTransportes
from entregasDeLosAlpes.modulos.vehiculos.dominio.entidades import Transporte
from dataclasses import dataclass
from .base import TransporteQueryBaseHandler
from entregasDeLosAlpes.modulos.vehiculos.aplicacion.mapeadores import MapeadorTransporte
import uuid

@dataclass
class EntregarProducto(Query):
    id: str

class EntregarProductoHandler(TransporteQueryBaseHandler):

    def handle(self, query: EntregarProducto) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Transporte)
        transporte =  self.fabrica_vehiculos.crear_objeto(vista.obtener_por(id=query.id)[0], MapeadorTransporte())
        return QueryResultado(resultado=transporte)

@query.register(EntregarProducto)
def ejecutar_query_entregar_producto(query: EntregarProducto):
    handler = EntregarProductoHandler()
    return handler.handle(query)