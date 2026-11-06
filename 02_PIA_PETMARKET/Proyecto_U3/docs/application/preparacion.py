"""Operaciones de preparación sobre cada suborden, aisladas por almacén."""
from domain.model import EstadoPreparacion,ReglaNegocioError
from .autorizacion import Actor,exigir_almacen
from .contratos import ResumenPreparacion
class PreparacionApplicationService:
    def __init__(self,ordenes):self.ordenes=ordenes
    def cambiar_estado(self,actor:Actor,orden_id:str,nuevo:EstadoPreparacion)->ResumenPreparacion:
        orden=self.ordenes.obtener(orden_id)
        if orden is None:raise ReglaNegocioError('Suborden inexistente')
        exigir_almacen(actor,orden.almacen_id)
        orden.cambiar_estado(nuevo)
        self.ordenes.guardar(orden)
        return ResumenPreparacion(orden.id,orden.almacen_id,orden.estado.value,len(orden.lineas))
    def consultar_del_almacen(self,actor:Actor,pedido_id:str)->list[ResumenPreparacion]:
        if actor.rol!='ALMACEN' or not actor.almacen_id:
            raise ReglaNegocioError('Operador de almacén requerido')
        ordenes=[o for o in self.ordenes.listar_por_pedido(pedido_id) if o.almacen_id==actor.almacen_id]
        return [ResumenPreparacion(o.id,o.almacen_id,o.estado.value,len(o.lineas)) for o in ordenes]
