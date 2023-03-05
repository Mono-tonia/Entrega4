from pulsar.schema import *
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoRecibirOrdenPayload(ComandoIntegracion):
    id_cliente = String()
    # TODO Cree los records para itinerarios

class ComandoRecibirOrden(ComandoIntegracion):
    data = ComandoRecibirOrdenPayload()

class ComandoProcesarOrdenPayload(ComandoIntegracion):
    id_cliente = String()
    # TODO Cree los records para itinerarios

class ComandoProcesarOrden(ComandoIntegracion):
    data = ComandoProcesarOrdenPayload()