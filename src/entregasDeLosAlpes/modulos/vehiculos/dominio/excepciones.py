""" Excepciones del dominio de vehiculos

En este archivo usted encontrará los Excepciones relacionadas
al dominio de vehiculos

"""

from entregasDeLosAlpes.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioVehiculosExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de vehiculos'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)