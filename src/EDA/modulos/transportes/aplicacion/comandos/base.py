from EDA.seedwork.aplicacion.comandos import ComandoHandler
from EDA.modulos.transportes.infraestructura.fabricas import FabricaRepositorio
from EDA.modulos.transportes.dominio.fabricas import FabricaTransporte

class IniciarDistribucionBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_vuelos: FabricaTransporte = FabricaTransporte()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_transportes(self):
        return self._fabrica_transportes  
    