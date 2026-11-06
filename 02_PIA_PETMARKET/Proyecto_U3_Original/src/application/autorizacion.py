"""Control de roles para acciones administrativas o del almacén."""
from dataclasses import dataclass
from domain.model import ReglaNegocioError
@dataclass(frozen=True)
class Actor:
    identificador:str
    rol:str
    almacen_id:str|None=None

def exigir_admin(actor:Actor):
    if actor.rol!='ADMINISTRADOR' or not actor.identificador.strip():
        raise ReglaNegocioError('Se requiere un administrador autorizado')
def exigir_almacen(actor:Actor,almacen_id:str):
    if actor.rol!='ALMACEN' or actor.almacen_id!=almacen_id:
        raise ReglaNegocioError('El operador no pertenece a este almacén')
def exigir_cliente(actor:Actor,cliente_id:str):
    if actor.rol!='CLIENTE' or actor.identificador!=cliente_id:
        raise ReglaNegocioError('El pedido no corresponde al solicitante')
