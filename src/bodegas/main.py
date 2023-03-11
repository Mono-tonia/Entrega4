from fastapi import FastAPI
# from cliente.config.api import app_configs, settings
# from cliente.api.v1.router import router as v1

# from cliente.modulos.infraestructura.consumidores import suscribirse_a_topico
# from .eventos import EventoUsuario, UsuarioValidado, UsuarioDesactivado, UsuarioRegistrado, TipoCliente

# from cliente.modulos.infraestructura.despachadores import Despachador
# from cliente.seedwork.infraestructura import utils

import asyncio
import time
import traceback
import uvicorn

from pydantic import BaseSettings
from typing import Any

from .eventos import EventoConfirmacionBodega, ConfirmacionRevertida, EntregaConfirmada
from .comandos import ComandoConfirmarEntrega, ComandoRevertirConfirmacion, ConfirmarEntregaPayload, RevertirConfirmacionPayload
from .consumidores import suscribirse_a_topico
from .despachadores import Despachador

from . import utils

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "Vehiculos EntregasDeLosAlpes"}

app = FastAPI(**app_configs)
tasks = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(suscribirse_a_topico("evento-bodega", "sub-bodegas", EventoConfirmacionBodega))
    task2 = asyncio.ensure_future(suscribirse_a_topico("comando-confirmar-entrega", "sub-com-bodegas-confirmacion", ComandoConfirmarEntrega))
    task3 = asyncio.ensure_future(suscribirse_a_topico("comando-revertir-confirmacion", "sub-com-bodegas-revertir-confirmacion", ComandoRevertirConfirmacion))
    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get("/prueba-entrega-confirmada", include_in_schema=False)
async def prueba_entrega_confirmada() -> dict[str, str]:
    payload = EntregaConfirmada(
        id = "1232321321",
        id_correlacion = "389822434",
        orden_id = "6463454",
        fecha_confirmacion = utils.time_millis()
    )

    evento = EventoConfirmacionBodega(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=EntregaConfirmada.__name__,
        entrega_confirmada = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-bodega")
    return {"status": "ok"}

@app.get("/prueba-confirmacion-revertida", include_in_schema=False)
async def prueba_confirmacion_revertida() -> dict[str, str]:
    payload = ConfirmacionRevertida(
        id = "1232321321",
        id_correlacion = "389822434",
        orden_id = "6463454",
        fecha_actualizacion = utils.time_millis()
    )

    evento = EventoConfirmacionBodega(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ConfirmacionRevertida.__name__,
        vehiculo_cancelado = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-bodega")
    return {"status": "ok"}
    
@app.get("/prueba-confirmar-entrega", include_in_schema=False)
async def prueba_confirmar_entrega() -> dict[str, str]:
    payload = ConfirmarEntregaPayload(
        id_correlacion = "389822434",
        orden_id = "6463454",
    )

    comando = ComandoConfirmarEntrega(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ConfirmarEntregaPayload.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-confirmar-entrega")
    return {"status": "ok"}

@app.get("/prueba-revertir-confirmacion", include_in_schema=False)
async def prueba_revertir_confirmacion() -> dict[str, str]:
    payload = RevertirConfirmacionPayload(
        id = "1232321321",
        id_correlacion = "389822434",
        orden_id = "6463454",
    )

    comando = ComandoRevertirConfirmacion(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RevertirConfirmacionPayload.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-revertir-confirmacion")
    return {"status": "ok"}