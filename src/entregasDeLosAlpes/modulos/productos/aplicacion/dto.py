from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class RutaDTO(DTO):
    fecha_salida: str
    fecha_llegada: str
    origen: dict
    destino: dict

@dataclass
class ProductoDTO(DTO):
    codigo: str 
    nombre: str
    categoria: str

@dataclass(frozen=True)
class OrdenDTO(DTO):
    id_cliente: str = field(default_factory=str)
    estado: str = field(default_factory=str)
    listaProd: list[ProductoDTO] = field(default_factory=list)
    ruta: RutaDTO = field(default_factory=RutaDTO)