from pydispatch import dispatcher

from .handlers import HandlerOrdenIntegracion

from entregasDeLosAlpes.modulos.bodegas.dominio.eventos import CrearAlmacenamiento, BuscarAlmacenamiento

dispatcher.connect(HandlerOrdenIntegracion.handle_orden_recibida, signal=f'{CrearAlmacenamiento.__name__}Integracion')
dispatcher.connect(HandlerOrdenIntegracion.handle_orden_procesada, signal=f'{BuscarAlmacenamiento.__name__}Integracion')
