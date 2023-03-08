from entregasDeLosAlpes.seedwork.aplicacion.comandos import Comando
from entregasDeLosAlpes.modulos.bodegas.aplicacion.dto import  AlmacenamientoDTO, BodegaDTO, StockDTO
from .base import CrearAlmacenamientoBaseHandler   
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from entregasDeLosAlpes.modulos.bodegas.dominio.entidades import Almacenamiento
from entregasDeLosAlpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from entregasDeLosAlpes.modulos.bodegas.aplicacion.mapeadores import MapeadorAlmacenamiento
from entregasDeLosAlpes.modulos.bodegas.dominio.repositorios import RepositorioAlmacenamiento, RepositorioEventosAlmacenamiento

@dataclass
class CrearAlmacenamiento(Comando): 
    id_cliente: str   
    listaBod: list[BodegaDTO]


class CrearAlmacenamientoHandler(CrearAlmacenamientoBaseHandler):
    
    def handle(self, comando: CrearAlmacenamiento):
        almacenamiento_dto = AlmacenamientoDTO(
                id_cliente=comando.id_cliente
            ,   listaBod=comando.listaBod
            )

        almacenamiento: Almacenamiento = self.fabrica_productos.crear_objeto(almacenamiento_dto, MapeadorAlmacenamiento())
        almacenamiento.crear_almacenamiento(almacenamiento)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioAlmacenamiento)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosAlmacenamiento)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, almacenamiento, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(CrearAlmacenamiento)
def ejecutar_comando_crear_almacenamiento(comando: CrearAlmacenamiento):
    handler = CrearAlmacenamientoBaseHandler()
    handler.handle(comando)
    