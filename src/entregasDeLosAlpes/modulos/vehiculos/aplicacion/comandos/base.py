from entregasDeLosAlpes.seedwork.aplicacion.comandos import ComandoHandler
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.fabricas import FabricaRepositorio
from entregasDeLosAlpes.modulos.vehiculos.dominio.fabricas import FabricaVehiculos

class RecibirProductoBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_vehiculos: FabricaVehiculos = FabricaVehiculos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_vehiculos(self):
        return self._fabrica_vehiculos    
    