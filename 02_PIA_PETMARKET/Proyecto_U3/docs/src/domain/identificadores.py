"""Identificadores de objetos que cruzan fronteras de agregados."""
from dataclasses import dataclass
from .model import ReglaNegocioError
@dataclass(frozen=True)
class Identificador:
    valor: str
    def __post_init__(self):
        if not isinstance(self.valor, str) or not self.valor.strip():
            raise ReglaNegocioError('El identificador no puede estar vacío')
    def __str__(self): return self.valor
class PedidoId(Identificador): pass
class AlmacenId(Identificador): pass
class ProductoSKU(Identificador): pass
