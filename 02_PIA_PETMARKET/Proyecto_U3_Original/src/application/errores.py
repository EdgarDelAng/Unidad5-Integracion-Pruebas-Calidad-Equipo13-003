"""Conversión de errores funcionales en resultados legibles por interfaces."""
from dataclasses import dataclass
from domain.model import ReglaNegocioError
@dataclass(frozen=True)
class ResultadoOperacion:
    exito:bool
    codigo:str
    mensaje:str
def interpretar_error(error:Exception)->ResultadoOperacion:
    return ResultadoOperacion(False,'REGLA_NEGOCIO' if isinstance(error,ReglaNegocioError) else 'ERROR_TECNICO',str(error) if isinstance(error,ReglaNegocioError) else 'Error interno')
