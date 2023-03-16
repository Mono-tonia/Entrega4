import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from entregasDeLosAlpes.modulos.productos.infraestructura.schema.v1.eventos import EventoOrdenRecibida
from entregasDeLosAlpes.modulos.productos.infraestructura.schema.v1.comandos import ComandoRecibirOrden


from entregasDeLosAlpes.modulos.productos.infraestructura.proyecciones import ProyeccionOrdenesLista, ProyeccionOrdenesTotales
from entregasDeLosAlpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from entregasDeLosAlpes.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-orden', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='entregasDeLosAlpes-sub-eventos', schema=AvroSchema(EventoOrdenRecibida))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionOrdenesTotales(datos.fecha_recepcion, ProyeccionOrdenesTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionOrdenesLista(datos.id_orden, datos.id_cliente, datos.estado, datos.fecha_recepcion, datos.fecha_actualizacion), app=app)
            
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
        consumidor = cliente.subscribe('comando-recibir-orden', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='entregasDeLosAlpes-sub-comando-recibir-orden', schema=AvroSchema(ComandoRecibirOrden))

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