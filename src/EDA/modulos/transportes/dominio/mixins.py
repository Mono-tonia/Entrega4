"""Mixins del dominio de vuelos

En este archivo usted encontrará las Mixins con capacidades 
reusables en el dominio de vuelos

"""

from .entidades import Ruta

class FiltradoRutasMixin:

    def filtrar_mejores_rutas(self, rutas: list[Ruta]) -> list[Ruta]:
        # Logica compleja para filtrar itinerarios
        # TODO
        return rutas