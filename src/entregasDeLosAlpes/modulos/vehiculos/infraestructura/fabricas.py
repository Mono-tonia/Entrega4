""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vehiculos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vehiculos

"""

from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.dominio.fabricas import Fabrica
from entregasDeLosAlpes.seedwork.dominio.repositorios import Repositorio
from entregasDeLosAlpes.seedwork.infraestructura.vistas import Vista
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.vistas import VistaTransporte
from entregasDeLosAlpes.modulos.vehiculos.dominio.entidades import Transporte
from entregasDeLosAlpes.modulos.vehiculos.dominio.repositorios import RepositorioProveedores, RepositorioEventosTransportes, RepositorioTransportes
from .repositorios import RepositorioTransportesSQLAlchemy, RepositorioProveedoresSQLAlchemy, RepositorioEventosTransportesSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioTransportes:
            return RepositorioTransportesSQLAlchemy()
        elif obj == RepositorioProveedores:
            return RepositorioProveedoresSQLAlchemy()
        elif obj == RepositorioEventosTransportes:
            return RepositorioEventosTransportesSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')

@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Transporte:
            return VistaTransporte()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')