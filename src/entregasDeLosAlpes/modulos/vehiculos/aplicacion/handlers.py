from entregasDeLosAlpes.modulos.vehiculos.dominio.eventos import ProductoRecibido, ProductoEntregado
from entregasDeLosAlpes.seedwork.aplicacion.handlers import Handler
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.despachadores import Despachador

class HandlerTransporteIntegracion(Handler):

    @staticmethod
    def handle_producto_recibido(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-transporte')

    @staticmethod
    def handle_producto_entregado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-transporte')

  

    