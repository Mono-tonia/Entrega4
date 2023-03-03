from EDA.modulos.transportes.dominio.eventos import DistribucionIniciada, DistribucionTerminada
from EDA.seedwork.aplicacion.handlers import Handler
from EDA.modulos.transportes.infraestructura.despachadores import Despachador

class HandlerDistribucionIntegracion(Handler):

    @staticmethod
    def handle_distribucion_iniciada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-distribucion')

    @staticmethod
    def handle_distribucion_terminada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-distribucion')


    