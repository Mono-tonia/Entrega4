"""Reglas de negocio del dominio de bodegas

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from entregasDeLosAlpes.seedwork.dominio.reglas import ReglaNegocio
from .entidades import Bodega


#regla para verificar que una bodega sea valida
class BodegaValida(ReglaNegocio):
    bodega: Bodega

    def __init__(self, bodega, mensaje='La bodega propuesta es incorrecta'):
        super().__init__(mensaje)
        self.bodega = bodega

    def es_valido(self) -> bool:
        return isinstance(self.bodega, Bodega)