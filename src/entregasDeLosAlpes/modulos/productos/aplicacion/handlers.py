from entregasDeLosAlpes.modulos.productos.dominio.eventos import OrdenRecibida, OrdenProcesada
from entregasDeLosAlpes.seedwork.aplicacion.handlers import Handler
from entregasDeLosAlpes.modulos.productos.infraestructura.despachadores import Despachador

class HandlerOrdenIntegracion(Handler):

    @staticmethod
    def handle_orden_recibida(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-orden')

    @staticmethod
    def handle_orden_procesada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-orden')

    