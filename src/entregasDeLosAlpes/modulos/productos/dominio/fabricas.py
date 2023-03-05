from .entidades import Orden
from .reglas import MinimoUnProducto, RutaValida
from .excepciones import TipoObjetoNoExisteEnDominioOrdenesExcepcion
from entregasDeLosAlpes.seedwork.dominio.repositorios import Mapeador, Repositorio
from entregasDeLosAlpes.seedwork.dominio.fabricas import Fabrica
from entregasDeLosAlpes.seedwork.dominio.entidades import Entidad
from entregasDeLosAlpes.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaOrden(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            orden : Orden = mapeador.dto_a_entidad(obj)

            self.validar_regla(MinimoUnProducto(orden.listaProd))
            [self.validar_regla(RutaValida(orden.ruta))]
            
            return orden 

@dataclass
class FabricaProductos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Orden.__class__:
            fabrica_orden = _FabricaOrden()
            return fabrica_orden.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioOrdenesExcepcion()
