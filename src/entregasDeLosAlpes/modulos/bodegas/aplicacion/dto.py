from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.aplicacion.dto import DTO

@dataclass
class ProductoDTO(DTO):
    codigo: str 
    nombre: str
    categoria: str

@dataclass
class StockDTO(DTO):
    stock: list[ProductoDTO]

@dataclass
class BodegaDTO(DTO):
    nombre: str 
    ubicacion: str
    capacidad: str
    stock: StockDTO

@dataclass(frozen=True)
class AlmacenamientoDTO(DTO):
    id_cliente: str = field(default_factory=str)
    listaBod: list[BodegaDTO] = field(default_factory=list[BodegaDTO])
