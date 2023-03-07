from pydispatch import dispatcher

from .handlers import HandlerOrdenIntegracion

from entregasDeLosAlpes.modulos.vehiculos.dominio.eventos import ProductoRecibido, ProductoEntregado

dispatcher.connect(HandlerOrdenIntegracion.handle_producto_recibido, signal=f'{ProductoRecibido.__name__}Integracion')
dispatcher.connect(HandlerOrdenIntegracion.handle_producto_entregado, signal=f'{ProductoEntregado.__name__}Integracion')
