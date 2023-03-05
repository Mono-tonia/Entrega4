from entregasDeLosAlpes.seedwork.aplicacion.queries import QueryHandler
from entregasDeLosAlpes.modulos.productos.infraestructura.fabricas import FabricaVista
from entregasDeLosAlpes.modulos.productos.dominio.fabricas import FabricaProductos

class OrdenQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_productos: FabricaProductos = FabricaProductos()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_productos(self):
        return self._fabrica_productos