import entregasDeLosAlpes.seedwork.presentacion.api as api
import json
from entregasDeLosAlpes.modulos.productos.aplicacion.dto import ReservaDTO
from entregasDeLosAlpes.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from entregasDeLosAlpes.modulos.productos.aplicacion.mapeadores import MapeadorOrdenDTOJson
from entregasDeLosAlpes.modulos.productos.aplicacion.comandos.recibir_orden import RecibirOrden
from entregasDeLosAlpes.modulos.productos.aplicacion.queries.obtener_orden import ObtenerOrden
from pulsar.schema import *
import pulsar
from entregasDeLosAlpes.seedwork.aplicacion.comandos import ejecutar_commando
from entregasDeLosAlpes.seedwork.aplicacion.queries import ejecutar_query
from aeroalpes.seedwork.infraestructura import utils


bp = api.crear_blueprint('productos', '/productos')

@bp.route('/orden', methods=('POST',))
def obtener_orden_usando_comando():
    try:
        # NOTE Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar y 
        # no la defecto de SQLAlchemy
        session['uow_metodo'] = 'pulsar'

        orden_dict = request.json

        map_orden = MapeadorOrdenDTOJson()
        orden_dto = map_orden.externo_a_dto(orden_dict)

        comando = RecibirOrden(orden_dto.id_cliente, orden_dto.estado, orden_dto.listaProd, orden_dto.ruta)
        
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        servidor = cliente.create_producer('orden-topic')

        servidor.send(str(comando).encode())

        cliente.close()

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/orden', methods=('GET',))
@bp.route('/orden/<id>', methods=('GET',))
def dar_orden_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerOrden(id))
        map_orden = MapeadorOrdenDTOJson()
        
        return map_orden.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]