""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from entregasDeLosAlpes.seedwork.dominio.repositorios import Mapeador
from entregasDeLosAlpes.seedwork.infraestructura.utils import unix_time_millis
from entregasDeLosAlpes.modulos.productos.dominio.objetos_valor import Ruta
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Producto, Orden
from entregasDeLosAlpes.modulos.productos.dominio.eventos import OrdenProcesada, OrdenRecibida, EventoOrden

from .dto import Ordenes as OrdenDTO
from .dto import ruta as rutaDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosOrden(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def _init_(self):
        self.router = {
            OrdenRecibida: self._entidad_a_orden_recibida,
            OrdenProcesada: self._entidad_a_orden_procesada,
        }

    def obtener_tipo(self) -> type:
        return EventoOrden._class_

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_orden_recibida(self, entidad: OrdenRecibida, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import OrdenRecibidaPayload, EventoOrdenRecibida

            payload = OrdenRecibidaPayload(
                id_orden=str(evento.id_orden), 
                id_cliente=str(evento.id_cliente), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoOrdenRecibida(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'OrdenRecibida'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'entregasDeLosAlpes'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_orden_procesada(self, entidad: OrdenProcesada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import  OrdenProcesadaPayload, EventoOrdenProcesada
            payload = OrdenProcesadaPayload(
                id_orden=str(evento.id_orden), 
                id_cliente=str(evento.id_cliente), 
                estado=str(evento.estado), 
            )
            evento_integracion = EventoOrdenProcesada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'OrdenRecibida'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'entregasDeLosAlpes'
            evento_integracion.data = payload

            return evento_integracion
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad) 
            

    def entidad_a_dto(self, entidad: EventoOrden, version=LATEST_VERSION) -> OrdenDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad._class_, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: OrdenDTO, version=LATEST_VERSION) -> Orden:
        raise NotImplementedError

"""
class MapeadorOrden(Mapeador):
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

    def _procesar_ruta(self, ruta: any) -> list[rutaDTO]:
        rutas_dto = list()

        
        ruta_dto = rutaDTO()
        ruta_dto.destino_codigo = ruta.destino.codigo
        ruta_dto.origen_codigo = ruta.origen.codigo
        ruta_dto.fecha_salida = ruta.fecha_salida
        ruta_dto.fecha_llegada = ruta.fecha_llegada
        

        rutas_dto.append(ruta_dto)

        return rutas_dto

    def obtener_tipo(self) -> type:
        return Orden._class_

    def entidad_a_dto(self, entidad: Orden) -> OrdenDTO:
        
        orden_dto = OrdenDTO()
        orden_dto.fecha_recepcion = entidad.fecha_recepcion
        orden_dto.fecha_actualizacion = entidad.fecha_actualizacion
        orden_dto.id = str(entidad.id)

        productos_dto = list()
        
        for productos in entidad.listaProd:
            productos_dto.extend(self._procesar_producto(productos))

        orden_dto.productos = productos_dto

        return orden_dto

    def dto_a_entidad(self, dto: OrdenDTO) -> Orden:
        orden = Orden(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        orden.rutas = list()

        rutas_dto: list[rutaDTO] = dto.rutas

        orden.rutas.extend(self._procesar_ruta_dto(rutas_dto))
        
        return orden
"""