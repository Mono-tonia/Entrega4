from pydispatch import dispatcher

from .handlers import HandlerOrdenIntegracion

from entregasDeLosAlpes.modulos.productos.dominio.eventos import OrdenRecibida, OrdenProcesada

dispatcher.connect(HandlerOrdenIntegracion.handle_orden_recibida, signal=f'{OrdenRecibida.__name__}Integracion')
dispatcher.connect(HandlerOrdenIntegracion.handle_orden_procesada, signal=f'{OrdenProcesada.__name__}Integracion')
