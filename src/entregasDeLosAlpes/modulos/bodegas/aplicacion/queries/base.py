from entregasDeLosAlpes.seedwork.aplicacion.queries import QueryHandler
from entregasDeLosAlpes.modulos.bodegas.infraestructura.fabricas import FabricaVista
from entregasDeLosAlpes.modulos.bodegas.dominio.fabricas import FabricaBodegas

class AlmacenamientoQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_bodegas: FabricaBodegas = FabricaBodegas()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_bodegas(self):
        return self._fabrica_bodegas