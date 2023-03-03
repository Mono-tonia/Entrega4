"""Reglas de negocio del dominio de cliente

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from aeroalpes.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import Ruta
from .objetos_valor import Producto


class RutaValida(ReglaNegocio):

    ruta: Ruta

    def __init__(self, ruta, mensaje='La ruta propuesta es incorrecta'):
        super().__init__(mensaje)
        self.ruta = ruta

    def es_valido(self) -> bool:
        return self.ruta.destino != self.ruta.origen

class MinimoUnProducto(ReglaNegocio):
    productos: list[Producto]

    def __init__(self, productos, mensaje='La lista de productos debe tener al menos un producto'):
        super().__init__(mensaje)
        self.productos = productos

    def es_valido(self) -> bool:
        return len(self.productos) > 0 and isinstance(self.productos[0], Producto) 