from entregasDeLosAlpes.seedwork.aplicacion.dto import Mapeador as AppMap
from entregasDeLosAlpes.seedwork.dominio.repositorios import Mapeador as RepMap
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Orden
from .dto import RutaDTO, OrdenDTO, ProductoDTO

from datetime import datetime

class MapeadorOrdenDTOJson(AppMap):
    def _procesar_ruta(self, ruta: dict) -> RutaDTO:
        return RutaDTO
    
    def _procesar_producto(self, producto: dict) -> ProductoDTO:
        return ProductoDTO
        
    def externo_a_dto(self, externo: dict) -> OrdenDTO:
        orden_dto = OrdenDTO()

        for prod in externo.get('productos', list()):
            orden_dto.listaProd.append(self._procesar_producto(prod))

        return orden_dto

    def dto_a_externo(self, dto: OrdenDTO) -> dict:
        return dto.__dict__

class MapeadorOrden(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Orden.__class__        

    def entidad_a_dto(self, entidad: Orden) -> OrdenDTO:
        return OrdenDTO(Orden.id_cliente, Orden.estado, Orden.listaProd, Orden.ruta)
        
    def dto_a_entidad(self, dto: OrdenDTO) -> Orden:
        return Orden(OrdenDTO.id_cliente, OrdenDTO.estado, OrdenDTO.listaProd, OrdenDTO.ruta)



