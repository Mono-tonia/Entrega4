from .entidades import Compra
#from .reglas import MinimoUnItinerario, RutaValida
from .excepciones import TipoObjetoNoExisteEnDominioProductosExcepcion
from EDA.seedwork.dominio.repositorios import Mapeador, Repositorio
from EDA.seedwork.dominio.fabricas import Fabrica
from EDA.seedwork.dominio.entidades import Entidad
from EDA.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaCompra(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            compra : Compra = mapeador.dto_a_entidad(obj)


            #self.validar_regla(MinimoUnItinerario(compra .itinerarios))
           #[self.validar_regla(RutaValida(ruta)) for itin in compra .itinerarios for odo in itin.odos for segmento in odo.segmentos for ruta in segmento.legs]
            
            return compra 

@dataclass
class FabricaProductos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Compra.__class__:
            fabrica_compra = _FabricaCompra()
            return fabrica_compra.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioProductosExcepcion()
