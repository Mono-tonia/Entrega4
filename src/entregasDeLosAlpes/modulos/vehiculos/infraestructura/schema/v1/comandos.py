from pulsar.schema import *
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoRecibirProductoPayload(ComandoIntegracion):
    id_bodega = String()
    # TODO Cree los records para itinerarios

class ComandoRecibirProducto(ComandoIntegracion):
    data = ComandoRecibirProductoPayload()

class ComandoEntregarProductoPayload(ComandoIntegracion):
    id_cliente = String()
    # TODO Cree los records para itinerarios

class ComandoEntregarProducto(ComandoIntegracion):
    data = ComandoEntregarProductoPayload()