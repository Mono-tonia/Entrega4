import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from entregasDeLosAlpes.modulos.bodegas.infraestructura.schema.v1.eventos import EventoCrearAlmacenamiento
from entregasDeLosAlpes.modulos.bodegas.infraestructura.schema.v1.comandos import ComandoCrearAlmacenamiento


from entregasDeLosAlpes.modulos.bodegas.infraestructura.proyecciones import ProyeccionAlmacenamientoLista, ProyeccionAlmacenamientosTotales
from entregasDeLosAlpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from entregasDeLosAlpes.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-orden', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='entregasDeLosAlpes-sub-eventos', schema=AvroSchema(EventoCrearAlmacenamiento))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionAlmacenamientosTotales(datos.fecha_recepcion, ProyeccionOrdenesTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionAlmacenamientoLista(datos.id_cliente, datos.listaBod), app=app)
            
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
        consumidor = cliente.subscribe('comandos-orden', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='entregasDeLosAlpes-sub-comandos', schema=AvroSchema(ComandoCrearAlmacenamiento))

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