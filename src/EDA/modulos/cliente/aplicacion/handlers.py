

from EDA.modulos.cliente.dominio.eventos import ClienteCreado
from EDA.seedwork.aplicacion.handlers import Handler

class HandlerReservaDominio(Handler):

    @staticmethod
    def handle_reserva_creada(evento):
        print('================ CLIENTE CREADO ===========')
        

    