import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from entregasDeLosAlpes.modulos.vehiculos.infraestructura.schema.v1.eventos import EventoProductoEntregado, EventoProductoRecibido
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.schema.v1.comandos import ComandoEntregarProducto, ComandoRecibirProducto


from entregasDeLosAlpes.modulos.vehiculos.infraestructura.proyecciones import ProyeccionTransportesLista, ProyeccionTransportesTotales
from entregasDeLosAlpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from entregasDeLosAlpes.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-transporte', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='entregasDeLosAlpes-sub-eventos', schema=AvroSchema(EventoProductoEntregado))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionTransportesTotales(datos.fecha_recepcion, ProyeccionTransportesTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionTransportesLista(datos.id_transporte, datos.id_cliente, datos.id_bodega, datos.estado, datos.fecha_recepcion, datos.fecha_entrega), app=app)

            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-transporte', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='entregasDeLosAlpes-sub-comandos', schema=AvroSchema(EventoProductoEntregado))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()