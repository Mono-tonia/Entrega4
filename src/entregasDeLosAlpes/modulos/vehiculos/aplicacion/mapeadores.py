from entregasDeLosAlpes.seedwork.aplicacion.dto import Mapeador as AppMap
from entregasDeLosAlpes.seedwork.dominio.repositorios import Mapeador as RepMap
from entregasDeLosAlpes.modulos.vehiculos.dominio.entidades import Transporte, Proveedor, Producto
from entregasDeLosAlpes.modulos.vehiculos.dominio.objetos_valor import Ruta
from .dto import TransporteDTO, ProductoDTO, RutaDTO

from datetime import datetime

class MapeadorTransporteDTOJson(AppMap):
    def _procesar_ruta(self, ruta: dict) -> RutaDTO:
        return RutaDTO()
    
    def _procesar_producto(self, producto: dict) -> ProductoDTO:
        return ProductoDTO()
    
    def externo_a_dto(self, externo: dict) -> TransporteDTO:
        transporte_dto = TransporteDTO()

        for prod in externo.get('productos', list()):
            transporte_dto.productos.append(self._procesar_producto(prod))

        return transporte_dto

    def dto_a_externo(self, dto: TransporteDTO) -> dict:
        return dto.__dict__

class MapeadorTransporte(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Transporte.__class__

    def locacion_a_dict(self, locacion):
        if not locacion:
            return dict(codigo=None, nombre=None, fecha_actualizacion=None, fecha_creacion=None)
        
        return dict(
                    codigo=locacion.codigo
                ,   nombre=locacion.nombre
                ,   fecha_actualizacion=locacion.fecha_actualizacion.strftime(self._FORMATO_FECHA)
                ,   fecha_creacion=locacion.fecha_creacion.strftime(self._FORMATO_FECHA)
        )
        

    def entidad_a_dto(self, entidad: Transporte) -> TransporteDTO:
        
        _id = str(entidad.id)
        id_cliente = str(entidad.id_cliente)        
        id_bodega = str(entidad.id_bodega)
        fecha_recepcion = entidad.fecha_recepcion.strftime(self._FORMATO_FECHA)
        fecha_entrega = entidad.fecha_entrega.strftime(self._FORMATO_FECHA)
        productos = list()
        rutas = list()

        return TransporteDTO(_id, id_cliente, id_bodega, fecha_recepcion, fecha_entrega,productos,rutas)

    def dto_a_entidad(self, dto: TransporteDTO) -> Transporte:
     
        return Transporte(TransporteDTO._id, TransporteDTO.id_cliente, TransporteDTO.id_bodega, TransporteDTO.fecha_recepcion, TransporteDTO.fecha_entrega,TransporteDTO.productos,TransporteDTO.rutas)



