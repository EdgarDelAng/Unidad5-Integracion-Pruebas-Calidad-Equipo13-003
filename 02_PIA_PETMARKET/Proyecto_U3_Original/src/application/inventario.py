"""Lecturas del stock por almacén sin revelar entidades mutables."""
from .contratos import ExistenciaDTO
class InventarioApplicationService:
    def __init__(self,inventario):self.inventario=inventario
    def consultar(self,almacen_id:str,sku:str)->ExistenciaDTO|None:
        x=self.inventario.obtener(almacen_id,sku)
        return None if x is None else ExistenciaDTO(x.almacen_id,x.producto_sku,x.disponible,x.reservado)
