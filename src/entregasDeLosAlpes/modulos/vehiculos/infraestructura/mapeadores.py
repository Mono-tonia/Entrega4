""" Mapeadores para la capa de infrastructura del dominio de vehiculos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from entregasDeLosAlpes.seedwork.dominio.repositorios import Mapeador
from entregasDeLosAlpes.seedwork.infraestructura.utils import unix_time_millis
from entregasDeLosAlpes.modulos.vehiculos.dominio.objetos_valor import NombreProveedor, Codigo, Ruta
from entregasDeLosAlpes.modulos.vehiculos.dominio.entidades import Proveedor, Producto, Transporte
from entregasDeLosAlpes.modulos.vehiculos.dominio.eventos import ProductoEntregado, ProductoRecibido, EventoTransporte

from .dto import Transportes as TransporteDTO
from .dto import Productos as ProductoDTO
from .dto import Rutas as RutasDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosTransporte(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            ProductoRecibido: self._entidad_producto_recibido,
            ProductoEntregado: self._entidad_producto_entregado
        }

    def obtener_tipo(self) -> type:
        return EventoTransporte.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_producto_recibido(self, entidad: ProductoRecibido, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import ProductoRecibidoPayload, EventoProductoRecibido

            payload = ProductoRecibidoPayload(
                id_transporte=str(evento.id_transporte), 
                id_bodega=str(evento.id_bodega), 
                fecha_recepcion=int(unix_time_millis(evento.fecha_recepcion))
            )
            evento_integracion = EventoProductoRecibido(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_recepcion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'ProductoRecibido'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'entregasDeLosAlpes'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)     

    def _entidad_producto_entregado(self, entidad: ProductoEntregado, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import ProductoEntregadoPayload, EventoProductoEntregado

            payload = ProductoEntregadoPayload(
                id_transporte=str(evento.id_transporte), 
                id_cliente=str(evento.id_cliente), 
                fecha_entrega=int(unix_time_millis(evento.fecha_entrega))
            )
            evento_integracion = EventoProductoEntregado(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_entrega))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'ProductoRecibido'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'entregasDeLosAlpes'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)   

    def entidad_a_dto(self, entidad: EventoTransporte, version=LATEST_VERSION) -> TransporteDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: TransporteDTO, version=LATEST_VERSION) -> Transporte:
        raise NotImplementedError


class MapeadorTransporte(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'


    def _procesar_ruta_dto(self, ruta_dto: list) -> list[Ruta]:
        ruta_dict = dict()
        
        for ruta in ruta_dto:
            destino = Ruta(codigo=ruta.destino, nombre=None)
            origen = Ruta(codigo=ruta.origen, nombre=None)
            fecha_salida = ruta.fecha_salida
            fecha_llegada = ruta.fecha_llegada

           # ruta_dict.setdefault(str(ruta.odo_orden),{}).setdefault(str(itin.segmento_orden), {}).setdefault(str(itin.leg_orden), ruta(fecha_salida, fecha_llegada, origen, destino))

        #odos = list()
        #for k, odos_dict in itin_dict.items():
            #segmentos = list()
            #for k, seg_dict in odos_dict.items():
                #legs = list()
                #for k, ruta in seg_dict.items():
                    #legs.append(ruta)
                #segmentos.append(Segmento(legs))
            #odos.append(Odo(segmentos))

        return [Ruta()]
    
    def _procesar_ruta(self, ruta: any) -> list[RutasDTO]:
        rutas_dto = list()

        
        ruta_dto = RutasDTO()
        ruta_dto.destino_codigo = ruta.destino.codigo
        ruta_dto.origen_codigo = ruta.origen.codigo
        ruta_dto.fecha_salida = ruta.fecha_salida
        ruta_dto.fecha_llegada = ruta.fecha_llegada
        

        rutas_dto.append(ruta_dto)

        return rutas_dto

    def obtener_tipo(self) -> type:
        return Transporte._class_

    def entidad_a_dto(self, entidad: Transporte) -> TransporteDTO:
        
        transporte_dto = TransporteDTO()
        transporte_dto.fecha_recepcion = entidad.fecha_recepcion
        transporte_dto.fecha_entrega = entidad.fecha_entrega
        transporte_dto.id = str(entidad.id)

        productos_dto = list()
        
        for productos in entidad.listaProd:
            productos_dto.extend(self._procesar_producto(productos))

        transporte_dto.productos = productos_dto

        return transporte_dto

    def dto_a_entidad(self, dto: TransporteDTO) -> Transporte:
        transporte = Transporte(dto.id, dto.fecha_recepcion, dto.fecha_entrega)
        transporte.rutas = list()

        rutas_dto: list[RutasDTO] = dto.rutas

        transporte.rutas.extend(self._procesar_ruta_dto(rutas_dto))
        
        return transporte