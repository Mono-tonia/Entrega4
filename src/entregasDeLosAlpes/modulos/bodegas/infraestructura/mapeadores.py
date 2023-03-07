""" Mapeadores para la capa de infrastructura del dominio de Almacenamiento

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from entregasDeLosAlpes.seedwork.dominio.repositorios import Mapeador
from entregasDeLosAlpes.seedwork.infraestructura.utils import unix_time_millis
from entregasDeLosAlpes.modulos.bodegas.dominio.objetos_valor import Stock
from entregasDeLosAlpes.modulos.bodegas.dominio.entidades import Almacenamiento, Bodega
from entregasDeLosAlpes.modulos.bodegas.dominio.eventos import BuscarAlmacenamiento, CrearAlmacenamiento, EventoAlmacenamiento

from .dto import Almacenamiento as AlmacenamientoDTO
from .dto import Stock as StockDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosAlmacenamiento(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def _init_(self):
        self.router = {
            CrearAlmacenamiento: self._entidad_a_crear_almacenamiento,
            BuscarAlmacenamiento: self._entidad_a_buscar_almacenamiento,
        }

    def obtener_tipo(self) -> type:
        return EventoAlmacenamiento._class_

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_crear_almacenamiento(self, entidad: CrearAlmacenamiento, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import CrearAlmacenamientoPayload, EventoCrearAlmacenamiento

            payload = CrearAlmacenamientoPayload(
                id_cliente=str(evento.id_cliente),
                listaBod=evento.listaBod
            )
            evento_integracion = EventoCrearAlmacenamiento(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'CrearAlmacenamiento'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'entregasDeLosAlpes'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_buscar_almacenamiento(self, entidad: BuscarAlmacenamiento, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import  BuscarAlmacenamientoPayload, EventoBuscarAlmacenamiento
            payload = BuscarAlmacenamientoPayload(
                bodega=evento.bodega, 
                producto=evento.producto, 
                stock=evento.stock
            )
            evento_integracion = EventoBuscarAlmacenamiento(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'BuscarAlmacenamiento'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'entregasDeLosAlpes'
            evento_integracion.data = payload

            return evento_integracion
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad) 
            

    def entidad_a_dto(self, entidad: EventoAlmacenamiento, version=LATEST_VERSION) -> AlmacenamientoDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad._class_, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: AlmacenamientoDTO, version=LATEST_VERSION) -> Almacenamiento:
        raise NotImplementedError


class MapeadorAlmacenamiento(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    """
    def _procesar_ruta_dto(self, prod_dto: list) -> list[prod]: #Esto es el stock
        prod_dict = dict()
        
        for prod in prod_dto:
            destino = Ruta(codigo=ruta.destino, nombre=None)
            origen = Ruta(codigo=ruta.origen, nombre=None)
            fecha_salida = ruta.fecha_salida
            fecha_llegada = ruta.fecha_llegada

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
    """

    def obtener_tipo(self) -> type:
        return Almacenamiento._class_

    def entidad_a_dto(self, entidad: Almacenamiento) -> AlmacenamientoDTO:
        
        almacenamiento_dto = AlmacenamientoDTO()
        almacenamiento_dto.id_cliente = entidad.id_cliente
        almacenamiento_dto.ListaBodegas=entidad.listaBod

        return almacenamiento_dto

    def dto_a_entidad(self, dto: AlmacenamientoDTO) -> AlmacenamientoDTO:
        almacenamiento = Almacenamiento(dto.id_cliente, dto.ListaBodegas)       
        return almacenamiento
