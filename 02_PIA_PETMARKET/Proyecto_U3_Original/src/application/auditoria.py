"""Registro opcional de acciones; no contiene datos bancarios ni sensibles."""
from dataclasses import dataclass,field
from datetime import datetime,timezone
@dataclass(frozen=True)
class RegistroAccion:
    operacion:str
    objeto_id:str
    actor_id:str
    instante:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
class BitacoraOperaciones:
    def __init__(self):self.registros=[]
    def agregar(self,accion:RegistroAccion):self.registros.append(accion)
    def por_objeto(self,objeto_id:str):return [r for r in self.registros if r.objeto_id==objeto_id]
