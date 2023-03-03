from EDA.seedwork.aplicacion.comandos import Comando
from EDA.modulos.productos.aplicacion.dto import  CompraDTO
from .base import CrearCompraBaseHandler
from dataclasses import dataclass, field
from EDA.seedwork.aplicacion.comandos import ejecutar_commando as comando

from EDA.modulos.productos.dominio.entidades import Compra
from EDA.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from EDA.modulos.productos.aplicacion.mapeadores import MapeadorCompra
from EDA.modulos.productos.infraestructura.repositorios import RepositorioCompras, RepositorioEventosCompras

@dataclass
class CrearCompra(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    #itinerarios: list[ItinerarioDTO]


class CrearCompraHandler(CrearCompraBaseHandler):
    
    def handle(self, comando: CrearCompra):
        compra_dto = CompraDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            #,   itinerarios=comando.itinerarios
            )

        compra: Compra = self.fabrica_productos.crear_objeto(compra_dto, MapeadorCompra())
        compra.crear_compra(compra)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCompras)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosCompras)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, compra, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(CrearCompra)
def ejecutar_comando_crear_compra(comando: CrearCompra):
    handler = CrearCompraHandler()
    handler.handle(comando)
    