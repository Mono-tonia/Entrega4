from entregasDeLosAlpes.seedwork.aplicacion.queries import QueryHandler
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.fabricas import FabricaVista
from entregasDeLosAlpes.modulos.vehiculos.dominio.fabricas import FabricaVehiculos

class TransporteQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_vehiculos: FabricaVehiculos = FabricaVehiculos()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_vehiculos(self):
        return self._fabrica_vehiculos    