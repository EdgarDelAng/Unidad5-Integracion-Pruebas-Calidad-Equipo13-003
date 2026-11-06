"""Modelo de lectura con vistas reducidas, separado de escritura."""
from .services import PedidoDetalleDTO
from domain.model import ReglaNegocioError
class ConsultasApplicationService:
    def __init__(self,pedidos,envios):self.pedidos,self.envios=pedidos,envios
    def pedidos_del_cliente(self,cliente_id:str)->list[PedidoDetalleDTO]:
        return [PedidoDetalleDTO(p.id,p.estado.value,str(p.total),len(p.detalles)) for p in self.pedidos.listar() if p.cliente_id==cliente_id]
    def buscar_por_id(self,pedido_id:str)->PedidoDetalleDTO|None:
        p=self.pedidos.obtener(pedido_id)
        return None if p is None else PedidoDetalleDTO(p.id,p.estado.value,str(p.total),len(p.detalles))
    def incidencias_pendientes(self)->list[dict]:
        return [{'envio_id':e.id,'pedido_id':e.pedido_id,'incidencias':len(e.incidencias)}
                for e in self.envios.listar() if e.estado=='ENTREGA_FALLIDA']
