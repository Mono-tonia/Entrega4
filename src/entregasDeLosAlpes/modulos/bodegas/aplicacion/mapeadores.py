from entregasDeLosAlpes.seedwork.aplicacion.dto import Mapeador as AppMap
from entregasDeLosAlpes.seedwork.dominio.repositorios import Mapeador as RepMap
from entregasDeLosAlpes.modulos.bodegas.dominio.entidades import Almacenamiento
from .dto import AlmacenamientoDTO, BodegaDTO, StockDTO

from datetime import datetime

class MapeadorAlmacenamientoDTOJson(AppMap):
    def _procesar_stock(self, stock: dict) -> StockDTO:
        return StockDTO
    
    def _procesar_bodega(self, bodega: dict) -> BodegaDTO:
        return BodegaDTO
        
    def externo_a_dto(self, externo: dict) -> AlmacenamientoDTO:
        almacenamiento_dto = AlmacenamientoDTO()

        for bod in externo.get('bodegas', list()):
            almacenamiento_dto.listaBod.append(self._procesar_bodega(bod))

        return almacenamiento_dto

    def dto_a_externo(self, dto: AlmacenamientoDTO) -> dict:
        return dto.__dict__

class MapeadorAlmacenamiento(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Almacenamiento.__class__        

    def entidad_a_dto(self, entidad: Almacenamiento) -> AlmacenamientoDTO:
        return AlmacenamientoDTO(Almacenamiento.id_cliente, Almacenamiento.listaBod)
        
    def dto_a_entidad(self, dto: AlmacenamientoDTO) -> Almacenamiento:
        return Almacenamiento(Almacenamiento.id_cliente, Almacenamiento.listaBod)



