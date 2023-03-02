""" Interfaces para los repositorios del dominio de vuelos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de vuelos

"""

from abc import ABC
from EDA.seedwork.dominio.repositorios import Repositorio

class RepositorioClientes(Repositorio, ABC):
    ...

"""
class RepositorioEventosClientes(Repositorio, ABC):
    ...
"""