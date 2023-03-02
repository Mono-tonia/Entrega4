import EDA.seedwork.presentacion.api as api
import json
#from EDA.modulos.productos.aplicacion.dto import CompraDTO
#from EDA.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
#from EDA.modulos.productos.aplicacion.mapeadores import MapeadorCompraDTOJson
#from EDA.modulos.productos.aplicacion.comandos.crear_compra import CrearCompra
#from EDA.modulos.productos.aplicacion.queries.obtener_compra import ObtenerCompra
#from EDA.seedwork.aplicacion.comandos import ejecutar_commando
#from EDA.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('productos', '/productos')

@bp.route('/compra', methods=('POST',))
def comprar_usando_comando():
    try:
        # NOTE Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar y 
        # no la defecto de SQLAlchemy
        session['uow_metodo'] = 'pulsar'

        compra_dict = request.json

        map_compra = MapeadorCompraDTOJson()
        compra_dto = map_compra.externo_a_dto(compra_dict)

        comando = CrearCompra(compra_dto.fecha_creacion, compra_dto.fecha_actualizacion, compra_dto.id)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/compra', methods=('GET',))
@bp.route('/compra/<id>', methods=('GET',))
def dar_compra_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerCompra(id))
        map_compra = MapeadorCompraDTOJson()
        
        return map_compra.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]