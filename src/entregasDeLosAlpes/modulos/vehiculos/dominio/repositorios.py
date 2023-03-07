""" Interfaces para los repositorios del dominio de vehiculos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de vehiculos

"""

from abc import ABC
from entregasDeLosAlpes.seedwork.dominio.repositorios import Repositorio

class RepositorioTransportes(Repositorio, ABC):
    ...

class RepositorioEventosTransportes(Repositorio, ABC):
    ...

class RepositorioProveedores(Repositorio, ABC):
    ...