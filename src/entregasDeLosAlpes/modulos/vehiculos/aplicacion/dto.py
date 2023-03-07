from dataclasses import dataclass, field
from entregasDeLosAlpes.seedwork.aplicacion.dto import DTO

@dataclass (frozen=True)
class ProductoDTO(DTO):
    codigo: str 
    nombre: str
    categoria: str

@dataclass(frozen=True)
class RutaDTO(DTO):
    fecha_salida: str
    fecha_llegada: str
    destino: dict

@dataclass(frozen=True)
class TransporteDTO(DTO):
    id: str = field(default_factory=str)
    id_cliente: str = field(default_factory=str)
    id_bodega: str = field(default_factory=str)
    fecha_recepcion: str = field(default_factory=str)
    fecha_entrega: str = field(default_factory=str)
    productos: list[ProductoDTO] = field(default_factory=list)
    rutas: list[RutaDTO] = field(default_factory=list)