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

from .eventos import EventoVehiculo, ProductoEntregado, ProductoDevuelto
from .comandos import ComandoRecibirProducto, ComandoDevolverProducto, RecibirProductoPayload, DevolverProductoPayload
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
    task1 = asyncio.ensure_future(suscribirse_a_topico("evento-vehiculo", "sub-vehiculos", EventoVehiculo))
    task2 = asyncio.ensure_future(suscribirse_a_topico("comando-entregar-producto", "sub-com-vehiculos-entregar", ComandoRecibirProducto))
    task3 = asyncio.ensure_future(suscribirse_a_topico("comando-devolver-producto", "sub-com-vehiculos-devolver-producto", ComandoDevolverProducto))
    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get("/prueba-producto-entregado", include_in_schema=False)
async def prueba_producto_entregado() -> dict[str, str]:
    payload = ProductoEntregado(
        id = "1232321321",
        id_correlacion = "389822434",
        producto_id = "6463454",
        fecha_entrega = utils.time_millis()
    )

    evento = EventoVehiculo(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ProductoEntregado.__name__,
        producto_entregado = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-vehiculo")
    return {"status": "ok"}

@app.get("/prueba-producto-devuelto", include_in_schema=False)
async def prueba_producto_devuelto() -> dict[str, str]:
    payload = ProductoDevuelto(
        id = "1232321321",
        id_correlacion = "389822434",
        producto_id = "6463454",
        fecha_devolucion = utils.time_millis()
    )

    evento = EventoVehiculo(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ProductoDevuelto.__name__,
        producto_devuelto = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-vehiculo")
    return {"status": "ok"}
    
@app.get("/prueba-entregar-producto", include_in_schema=False)
async def prueba_entregar_producto() -> dict[str, str]:
    payload = RecibirProductoPayload(
        id_correlacion = "389822434",
        producto_id = "6463454",
    )

    comando = ComandoRecibirProducto(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RecibirProductoPayload.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-entregar-producto")
    return {"status": "ok"}

@app.get("/prueba-devolver-producto", include_in_schema=False)
async def prueba_devolver_producto() -> dict[str, str]:
    payload = DevolverProductoPayload(
        id = "1232321321",
        id_correlacion = "389822434",
        producto_id = "6463454",
    )

    comando = ComandoDevolverProducto(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=DevolverProductoPayload.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-devolver-producto")
    return {"status": "ok"}