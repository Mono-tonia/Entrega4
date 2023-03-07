""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.dominio.fabricas import Fabrica
from entregasDeLosAlpes.seedwork.dominio.repositorios import Repositorio
from entregasDeLosAlpes.seedwork.infraestructura.vistas import Vista
from entregasDeLosAlpes.modulos.bodegas.infraestructura.vistas import VistaAlmacenamiento
from entregasDeLosAlpes.modulos.bodegas.dominio.entidades import Almacenamiento
from entregasDeLosAlpes.modulos.bodegas.dominio.repositorios import RepositorioAlmacenamiento, RepositorioEventosAlmacenamiento
from .repositorios import RepositorioAlmacenamientoSQLAlchemy, RepositorioEventosAlmacenamientoSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioAlmacenamiento:
            return RepositorioAlmacenamientoSQLAlchemy()
        elif obj == RepositorioEventosAlmacenamiento:
            return RepositorioEventosAlmacenamientoSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')

@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Almacenamiento:
            return VistaAlmacenamiento()
        else:
            raise VistaAlmacenamiento(f'No existe fábrica para el objeto {obj}')