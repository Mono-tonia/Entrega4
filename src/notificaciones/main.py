import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import os
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Producto
from entregasDeLosAlpes.modulos.productos.dominio.objetos_valor import Ruta

def time_millis():
    return int(time.time() * 1000)

class EventoIntegracion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()

class OrdenRecibidaPayload(Record):
    id_orden = String()
    id_cliente = String()
    estado = String()
    producto = Producto
    ruta = Ruta()

class EventoOrdenRecibida(EventoIntegracion):
    data = OrdenRecibidaPayload()

HOSTNAME = os.getenv('PULSAR_ADDRESS', default="localhost")

client = pulsar.Client(f'pulsar://{HOSTNAME}:6650')
consumer = client.subscribe('eventos-orden', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='sub-notificacion-eventos-orden', schema=AvroSchema(EventoOrdenRecibida))

while True:
    msg = consumer.receive()
    print('=========================================')
    print("Mensaje Recibido: '%s'" % msg.value().data)
    print('=========================================')

    print('==== Envía correo a usuario ====')

    consumer.acknowledge(msg)

client.close()