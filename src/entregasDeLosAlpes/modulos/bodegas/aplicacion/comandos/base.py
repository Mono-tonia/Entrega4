from entregasDeLosAlpes.seedwork.aplicacion.comandos import ComandoHandler
from entregasDeLosAlpes.modulos.bodegas.infraestructura.fabricas import FabricaRepositorio
from entregasDeLosAlpes.modulos.bodegas.dominio.fabricas import FabricaBodegas

class CrearAlmacenamientoBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_bodegas: FabricaBodegas = FabricaBodegas()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_bodegas(self):
        return self._fabrica_bodegas
    