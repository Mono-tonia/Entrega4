from entregasDeLosAlpes.seedwork.aplicacion.comandos import Comando
from entregasDeLosAlpes.modulos.productos.aplicacion.dto import  OrdenDTO, ProductoDTO, RutaDTO
from .base import RecibirOrdenBaseHandler
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from entregasDeLosAlpes.modulos.productos.dominio.entidades import Orden
from entregasDeLosAlpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from entregasDeLosAlpes.modulos.productos.aplicacion.mapeadores import MapeadorOrden
from entregasDeLosAlpes.modulos.productos.dominio.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes

@dataclass
class RecibirOrden(Comando): 
    id_cliente: str   
    estado: str
    listaProd: list[ProductoDTO]
    ruta: RutaDTO


class RecibirOrdenHandler(RecibirOrdenBaseHandler):
    
    def handle(self, comando: RecibirOrden):
        orden_dto = OrdenDTO(
                id_cliente=comando.id_cliente
            ,   estado=comando.estado
            ,   listaProd=comando.listaProd
            ,   ruta=comando.ruta
            )

        orden: Orden = self.fabrica_productos.crear_objeto(orden_dto, MapeadorOrden())
        orden.recibir_orden(orden)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosOrdenes)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, orden, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(RecibirOrden)
def ejecutar_comando_crear_compra(comando: RecibirOrden):
    handler = RecibirOrdenHandler()
    handler.handle(comando)
    