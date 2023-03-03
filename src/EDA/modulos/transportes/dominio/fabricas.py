""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Distribucion
from .reglas import MinimoUnProducto, RutaValida
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from EDA.seedwork.dominio.repositorios import Mapeador, Repositorio
from EDA.seedwork.dominio.fabricas import Fabrica
from EDA.seedwork.dominio.entidades import Entidad
from EDA.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaDistribucion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            distribucion: Distribucion = mapeador.dto_a_entidad(obj)

            self.validar_regla(MinimoUnProducto(distribucion.productos))
            [self.validar_regla(RutaValida(ruta)) for itin in distribucion.productos for odo in itin.odos for segmento in odo.segmentos for ruta in segmento.legs]
            
            return distribucion

@dataclass
class FabricaTransporte(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Distribucion.__class__:
            fabrica_transporte = _FabricaDistribucion()
            return fabrica_transporte.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()

