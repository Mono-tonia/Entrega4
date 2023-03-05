""" Interfaces para los repositorios del dominio de bodegas

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de bodegas

"""

from abc import ABC
from entregasDeLosAlpes.seedwork.dominio.repositorios import Repositorio

class RepositorioAlmacenamiento(Repositorio, ABC):
    ...

class RepositorioEventosAlmacenamiento(Repositorio, ABC):
    ...
