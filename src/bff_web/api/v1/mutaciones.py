import strawberry
import typing

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    # TODO Agregue objeto de itinerarios o reserva
    @strawberry.mutation
    async def recibir_orden(self, id_cliente: str, id_correlacion: str, estado:str, info: Info) -> OrdenRespuesta:
        print(f"ID Cliente: {id_cliente}, ID Correlación: {id_correlacion}")
        payload = dict(
            id_cliente = id_cliente,
            estado=estado,
            id_correlacion = id_correlacion
        )
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoOrden",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web",
            data = payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-recibir-orden", "public/default/comando-recibir-orden")
        
        return OrdenRespuesta(mensaje="Procesando Mensaje", codigo=203)