from entregasDeLosAlpes.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from entregasDeLosAlpes.seedwork.aplicacion.queries import ejecutar_query as query
from entregasDeLosAlpes.modulos.productos.dominio.repositorios import RepositorioOrdenes
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Orden
from entregasDeLosAlpes.modulos.productos.aplicacion.dto import OrdenDTO
from dataclasses import dataclass
from .base import OrdenQueryBaseHandler
from entregasDeLosAlpes.modulos.productos.aplicacion.mapeadores import MapeadorOrden
import uuid

@dataclass
class ObtenerTodasOrdenes(Query):
    ...

class ObtenerTodasOrdenesHandler(OrdenQueryBaseHandler):

    def handle(self, query) -> QueryResultado:
        ordenes_dto = []
        vista = self.fabrica_vista.crear_objeto(Orden)
        ordenes = vista.obtener_todos()

        for orden in ordenes:
            dto = OrdenDTO(
                id_cliente=orden.id_cliente,
                estado=orden.estado,
                id = orden.id
            )
            ordenes_dto.append(dto)
        
        return QueryResultado(resultado=ordenes_dto)

@query.register(ObtenerTodasOrdenes)
def ejecutar_query_obtener_orden(query: ObtenerTodasOrdenes):
    handler = ObtenerTodasOrdenesHandler()
    return handler.handle(query)