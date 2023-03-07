""" Fábricas para la creación de objetos del dominio de vehiculos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vehiculos

"""

from .entidades import Transporte
from .reglas import MinimoUnProducto, RutaValida
from .excepciones import TipoObjetoNoExisteEnDominioVehiculosExcepcion
from entregasDeLosAlpes.seedwork.dominio.repositorios import Mapeador
from entregasDeLosAlpes.seedwork.dominio.fabricas import Fabrica
from entregasDeLosAlpes.seedwork.dominio.entidades import Entidad
from entregasDeLosAlpes.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaTransporte(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            transporte: Transporte = mapeador.dto_a_entidad(obj)

            self.validar_regla(MinimoUnProducto(transporte.productos))
            [self.validar_regla(RutaValida(transporte.ruta))]
            
            return transporte

@dataclass
class FabricaVehiculos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Transporte.__class__:
            fabrica_transporte = _FabricaTransporte()
            return fabrica_transporte.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioVehiculosExcepcion()

