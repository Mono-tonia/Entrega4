from EDA.seedwork.aplicacion.queries import QueryHandler
from EDA.modulos.transportes.infraestructura.fabricas import FabricaVista
from EDA.modulos.transportes.dominio.fabricas import FabricaTransporte

class DistribucionQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_transporte: FabricaTransporte = FabricaTransporte()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_transporte(self):
        return self._fabrica_transporte 