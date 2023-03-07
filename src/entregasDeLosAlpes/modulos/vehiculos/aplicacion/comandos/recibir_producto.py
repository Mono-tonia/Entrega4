from entregasDeLosAlpes.seedwork.aplicacion.comandos import Comando
from entregasDeLosAlpes.modulos.vehiculos.aplicacion.dto import TransporteDTO, ProductoDTO, RutaDTO
from .base import RecibirProductoBaseHandler
from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from entregasDeLosAlpes.modulos.vehiculos.dominio.entidades import Transporte
from entregasDeLosAlpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from entregasDeLosAlpes.modulos.vehiculos.aplicacion.mapeadores import MapeadorTransporte
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.repositorios import RepositorioTransportes, RepositorioEventosTransportes

@dataclass
class RecibirProducto(Comando):
    id: str
    id_cliente: str
    id_bodega: str
    fecha_recepcion: str
    fecha_entrega: str    
    productos: list[ProductoDTO]
    rutas: list[RutaDTO]

class RecibirProductoHandler(RecibirProductoBaseHandler):
    
    def handle(self, comando: RecibirProducto):
        transporte_dto = TransporteDTO(
                id=comando.id
            ,   id_cliente=comando.id_cliente
            ,   id_bodega=comando.id_bodega
            ,   fecha_recepcion=comando.fecha_recepcion
            ,   fecha_entrega=comando.fecha_entrega
            ,   productos=comando.productos
            ,   rutas=comando.rutas)

        transporte: Transporte = self.fabrica_vehiculos.crear_objeto(transporte_dto, MapeadorTransporte())
        transporte.recibir_producto(transporte)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTransportes)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosTransportes)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, transporte, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(RecibirProducto)
def ejecutar_comando_recibir_producto(comando: RecibirProducto):
    handler = RecibirProductoHandler()
    handler.handle(comando)
    