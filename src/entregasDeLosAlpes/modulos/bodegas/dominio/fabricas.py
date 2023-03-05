from .entidades import Almacenamiento
from .reglas import BodegaValida
from .excepciones import TipoObjetoNoExisteEnDominioAlmacenamientoExcepcion
from entregasDeLosAlpes.seedwork.dominio.repositorios import Mapeador, Repositorio
from entregasDeLosAlpes.seedwork.dominio.fabricas import Fabrica
from entregasDeLosAlpes.seedwork.dominio.entidades import Entidad
from entregasDeLosAlpes.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaAlmacenamiento(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            almacenamiento : Almacenamiento = mapeador.dto_a_entidad(obj)

            self.validar_regla(BodegaValida(almacenamiento.bodega))
            
            return almacenamiento 

@dataclass
class FabricaBodegas(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Almacenamiento.__class__:
            fabrica_almacenamiento = _FabricaAlmacenamiento()
            return fabrica_almacenamiento.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAlmacenamientoExcepcion()
