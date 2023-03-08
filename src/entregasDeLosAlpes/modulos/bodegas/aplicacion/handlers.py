from entregasDeLosAlpes.modulos.bodegas.dominio.eventos import CrearAlmacenamiento, BuscarAlmacenamiento
from entregasDeLosAlpes.seedwork.aplicacion.handlers import Handler
from entregasDeLosAlpes.modulos.bodegas.infraestructura.despachadores import Despachador

class HandlerAlmacenamientoIntegracion(Handler):

    @staticmethod
    def handle_crear_almacenamiento(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-almacenamiento')

    @staticmethod
    def handle_buscar_almacenamiento(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-almacenamiento')

    