from EDA.seedwork.aplicacion.comandos import Comando
from EDA.modulos.transportes.aplicacion.dto import ProductosDTO, DistribucionDTO
from .base import IniciarDistribucionBaseHandler
from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from EDA.modulos.transportes.dominio.entidades import Distribucion
from EDA.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from EDA.modulos.transportes.aplicacion.mapeadores import MapeadorDistribucion
from EDA.modulos.transportes.infraestructura.repositorios import RepositorioDistribuciones, RepositorioEventosDistribuciones

@dataclass
class IniciarDistribucion(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    productos: list[ProductosDTO]


class IniciarDistribucionHandler(IniciarDistribucionBaseHandler):
    
    def handle(self, comando: IniciarDistribucion):
        distribucion_dto = DistribucionDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   productos=comando.productos)

        distribucion: Distribucion = self.fabrica_transportes.crear_objeto(distribucion_dto, MapeadorDistribucion())
        distribucion.iniciar_distribucion(distribucion)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioDistribuciones)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosDistribuciones)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, distribucion, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(IniciarDistribucion)
def ejecutar_comando_iniciar_distribucion(comando: IniciarDistribucion):
    handler = IniciarDistribucionHandler()
    handler.handle(comando)
    