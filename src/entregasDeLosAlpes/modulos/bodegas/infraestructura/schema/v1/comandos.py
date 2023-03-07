from pulsar.schema import *
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearAlmacenamientoPayload(ComandoIntegracion):
    id_cliente = String()


class ComandoCrearAlmacenamiento(ComandoIntegracion):
    data = ComandoCrearAlmacenamientoPayload()

class ComandoBuscarAlmacenamientoPayload(ComandoIntegracion):
    id_cliente = String()

class ComandoBuscarAlmacenamiento(ComandoIntegracion):
    data = ComandoBuscarAlmacenamientoPayload()