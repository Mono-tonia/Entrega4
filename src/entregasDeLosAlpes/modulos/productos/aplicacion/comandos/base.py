from entregasDeLosAlpes.seedwork.aplicacion.comandos import ComandoHandler
from entregasDeLosAlpes.modulos.productos.infraestructura.fabricas import FabricaRepositorio
from entregasDeLosAlpes.modulos.productos.dominio.fabricas import FabricaProductos

class RecibirOrdenBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_productos: FabricaProductos = FabricaProductos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_productos(self):
        return self._fabrica_productos    
    